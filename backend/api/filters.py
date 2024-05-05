from django.contrib.auth import get_user_model
from django.forms import BooleanField
from django_filters import (
    CharFilter,
    ModelMultipleChoiceFilter,
    Filter,
)
from django_filters.rest_framework import FilterSet

from recipes.models import Ingredient, Recipe, Tag

User = get_user_model()


class BooleanFilter(Filter):
    """Переопределенный класс, только `True` или `False`"""

    field_class = BooleanField


class IngredientFilterSet(FilterSet):
    """Фильтр для Ингредиентов"""

    name = CharFilter(lookup_expr='istartswith')

    class Meta:
        model = Ingredient
        fields = ('name',)


class RecipeFilterSet(FilterSet):
    """Фильтр для Рецептов"""

    tags = ModelMultipleChoiceFilter(
        field_name='tags__slug',
        queryset=Tag.objects.all(),
        to_field_name='slug',
    )
    is_favorited = BooleanFilter(
        method='is_favorite_filter', field_name='favorites__author'
    )
    is_in_shopping_cart = BooleanFilter(
        method='is_in_shopping_cart_filter', field_name='shopping_cart__author'
    )

    class Meta:
        model = Recipe
        fields = ('author', 'tags', 'is_favorited', 'is_in_shopping_cart')
        ordering = ('id',)

    def is_favorite_filter(self, queryset, name, value):
        return self.filter_from_kwargs(queryset, value, name)

    def is_in_shopping_cart_filter(self, queryset, name, value):
        return self.filter_from_kwargs(queryset, value, name)

    def filter_from_kwargs(self, queryset, value, name):
        if value and self.request.user.id:
            return queryset.filter(**{name: self.request.user})
        return queryset