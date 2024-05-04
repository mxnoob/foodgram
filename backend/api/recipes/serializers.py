from django.db import transaction
from rest_framework import serializers

from api.fileds import Base64ImageField
from api.users.serializers import UserSerializer
from recipes.models import (
    Tag,
    Ingredient,
    Recipe,
    RecipeIngredient,
    FavoriteRecipe,
    ShoppingCart,
)


class TagSerializer(serializers.ModelSerializer):
    """Сериалайзер Тегов"""

    class Meta:
        model = Tag
        fields = ('id', 'name', 'slug')


class IngredientSerializer(serializers.ModelSerializer):
    """Сериалайзер ингредиента"""

    class Meta:
        model = Ingredient
        fields = ('id', 'name', 'measurement_unit')


class IngredientGetSerializer(serializers.ModelSerializer):
    """Сериалайзер представления ингредиента для рецепта"""

    id = serializers.IntegerField(source='ingredient.id')
    name = serializers.CharField(source='ingredient.name')
    measurement_unit = serializers.CharField(
        source='ingredient.measurement_unit'
    )

    class Meta:
        model = RecipeIngredient
        fields = ('id', 'name', 'measurement_unit', 'amount')


class RecipeSerializer(serializers.ModelSerializer):
    """Сериалайзер Рецепта"""

    author = UserSerializer(read_only=True)
    image = Base64ImageField()
    tags = TagSerializer(many=True)
    ingredients = IngredientGetSerializer(
        many=True, source='recipe_ingredients'
    )
    is_favorited = serializers.BooleanField(default=False, read_only=True)
    is_in_shopping_cart = serializers.BooleanField(
        default=False, read_only=True
    )

    class Meta:
        model = Recipe
        fields = (
            'id',
            'tags',
            'author',
            'ingredients',
            'is_favorited',
            'is_in_shopping_cart',
            'name',
            'image',
            'text',
            'cooking_time',
        )


class RecipeIngredientSerializer(serializers.ModelSerializer):
    """Сериалайзер короткого представления ингредиента для рецепта"""

    id = serializers.IntegerField()

    class Meta:
        model = RecipeIngredient
        fields = ('id', 'amount')


class RecipeCreateSerializer(serializers.ModelSerializer):
    """Сериалайзер создания Рецептов"""

    tags = serializers.PrimaryKeyRelatedField(
        queryset=Tag.objects.all(), many=True
    )
    ingredients = RecipeIngredientSerializer(
        many=True, source='recipe_ingredients'
    )
    image = Base64ImageField()

    class Meta:
        model = Recipe
        fields = (
            'ingredients',
            'tags',
            'image',
            'name',
            'text',
            'cooking_time',
        )

    def validate(self, attrs):
        tags = attrs.get('tags', [])
        if len(tags) == 0:
            raise serializers.ValidationError('Выберите хотя бы 1 тэг.')

        if len(set(tags)) != len(tags):
            raise serializers.ValidationError('Теги должны быть уникальные.')

        ingredients = attrs.get('recipe_ingredients', [])
        if len(ingredients) == 0:
            raise serializers.ValidationError('Добавьте хотя бы 1 ингредиент.')
        id_ingredients = {ingredient['id'] for ingredient in ingredients}
        if len(ingredients) != len(id_ingredients):
            raise serializers.ValidationError(
                'Ингредиенты должны быть уникальными.'
            )

        # if any(
        #     filter(
        #         lambda ingredient: not Ingredient.objects.filter(
        #             id=ingredient['id']
        #         ).exists(),
        #         ingredients,
        #     )
        # ):
        #     raise serializers.ValidationError(
        #         'Попытка добавить в рецепт несуществующие ингредиенты.'
        #     )

        for ingredient in ingredients:
            amount = ingredient['amount']
            if (
                isinstance(amount, str)
                and amount.isdigit()
                and int(amount) <= 0
            ) or amount <= 0:
                raise serializers.ValidationError(
                    'Количество ингредиентов должно быть больше 0.'
                )

        return attrs

    def create(self, validated_data):
        tags = validated_data.pop('tags')
        ingredients = validated_data.pop('recipe_ingredients')
        with transaction.atomic():
            recipe = Recipe.objects.create(**validated_data)
            self.add_tags_and_ingredients_to_recipe(recipe, tags, ingredients)
            return recipe

    def update(self, instance, validated_data):
        tags = validated_data.pop('tags')
        ingredients = validated_data.pop('recipe_ingredients')
        with transaction.atomic():
            self.add_tags_and_ingredients_to_recipe(
                instance, tags, ingredients, True
            )
            super().update(instance, validated_data)
            instance.save()
            return instance

    @staticmethod
    def add_tags_and_ingredients_to_recipe(
        recipe, tags, ingredients, updated=False
    ):
        """Добавление или обновление Тегов и Ингредиентов"""
        if updated:
            recipe.ingredients.clear()
            recipe.tags.clear()

        recipe.tags.set(tags)
        RecipeIngredient.objects.bulk_create(
            RecipeIngredient(
                recipe=recipe,
                ingredient_id=ingredient['id'],
                amount=ingredient['amount'],
            )
            for ingredient in ingredients
        )

    def to_representation(self, instance):
        return RecipeSerializer(instance, context=self.context).data


class ShortRecipeSerializer(serializers.ModelSerializer):
    """Сериалайзер представления ответа укороченных данных о Рецепте"""

    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time')


class AuthorRecipeSerializer(serializers.ModelSerializer):
    """Сериалайзер для наследования моделей вида Автор и Рецепт"""

    _recipe_added_to = None

    class Meta:
        model = None
        fields = '__all__'
        read_only_fields = ('author',)

    def validate(self, attrs):
        recipe = attrs['recipe']
        user = self.context['request'].user
        if self.Meta.model.objects.filter(author=user, recipe=recipe).exists():
            raise serializers.ValidationError(
                f'Рецепт уже добавлен в {self._recipe_added_to}'
            )
        return attrs

    def to_representation(self, instance):
        return ShortRecipeSerializer(
            instance.recipe, context=self.context
        ).data


class FavoriteSerializer(AuthorRecipeSerializer):
    """Сериалайзер Избранных рецептов"""

    _recipe_added_to = 'избранное'

    class Meta(AuthorRecipeSerializer.Meta):
        model = FavoriteRecipe


class ShoppingCartSerializer(AuthorRecipeSerializer):
    """Сериалайзер Корзины"""

    _recipe_added_to = 'корзину'

    class Meta(AuthorRecipeSerializer.Meta):
        model = ShoppingCart
