from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from api.fileds import Base64ImageField
from users.models import Subscriber

RECIPE_LIMIT = 3

User = get_user_model()


class ShortUserSerializer(serializers.ModelSerializer):
    """Сериализатор сокращенных полей пользователя"""

    class Meta:
        model = User
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
        )


class UserCreateSerializer(serializers.ModelSerializer):
    """Сериализатор создания пользователя"""

    class Meta:
        model = User
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'password',
        )
        extra_kwargs = {
            'first_name': {'required': True},
            'last_name': {'required': True},
        }
        write_only_fields = ('password',)

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user

    def to_representation(self, instance):
        return ShortUserSerializer(instance).data


class UserSerializer(serializers.ModelSerializer):
    """Сериализатор пользователя"""

    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'is_subscribed',
            'avatar',
        )

    def get_is_subscribed(self, obj):
        current_user = self.context.get('request').user
        if hasattr(obj, 'subs'):
            return obj.subs and obj.subs[0].is_subscribed
        return (
            current_user.is_authenticated
            and current_user != obj
            and obj.subscribers.filter(user=current_user).exists()
        )


class AvatarSerializer(serializers.ModelSerializer):
    """Сериализатор аватарки"""

    avatar = Base64ImageField(allow_null=True, required=True)

    class Meta:
        model = User
        fields = ('avatar',)


class UserRecipeSerializer(UserSerializer):
    """Сериплизатор представления рецептов пользователя"""

    recipes = serializers.SerializerMethodField()
    recipes_count = serializers.IntegerField(
        read_only=True, source='recipes.count'
    )

    class Meta:
        model = User
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'is_subscribed',
            'recipes',
            'recipes_count',
            'avatar',
        )

    def get_recipes(self, obj):
        from api.recipes.serializers import ShortRecipeSerializer

        request = self.context.get('request')
        recipes_limit = int(
            request.query_params.get('recipes_limit', RECIPE_LIMIT)
        )
        return ShortRecipeSerializer(
            obj.recipes.all()[:recipes_limit], many=True
        ).data


class SubscribeSerializer(serializers.ModelSerializer):
    """Сериализатор подписок"""

    user = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username',
        default=serializers.CurrentUserDefault(),
    )
    author = serializers.SlugRelatedField(
        slug_field='username',
        queryset=User.objects.all(),
    )

    class Meta:
        model = Subscriber
        fields = ('author', 'user')
        validators = [
            UniqueTogetherValidator(
                queryset=model.objects.all(),
                fields=('author', 'user'),
                message='Вы уже подписаны на этого пользователя',
            )
        ]

    def validate_author(self, author):
        if self.context['request'].user == author:
            raise serializers.ValidationError(
                'Нельзя подписаться на самого себя'
            )
        return author

    def to_representation(self, instance):
        return UserRecipeSerializer(instance.author, context=self.context).data