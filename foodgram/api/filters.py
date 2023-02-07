from django.db.models import Exists, OuterRef
from django_filters import rest_framework as filters

from recipes.models import Favorite, Recipe, ShoppingCart


class RecipeFilter(filters.FilterSet):
    """Фильтры рецептов."""

    is_favorited = filters.BooleanFilter(method='filter_bool')
    is_in_shopping_cart = filters.BooleanFilter(method='filter_bool')
    author = filters.CharFilter()
    tags = filters.Filter(method='filter_tags')

    class Meta:
        model = Recipe
        fields = ('is_favorited', 'is_in_shopping_cart', 'author', 'tags')

    def filter_bool(self, queryset, name, value):
        models = {
            'is_favorited': Favorite,
            'is_in_shopping_cart': ShoppingCart,
        }
        if self.request.user.is_authenticated and value == 1:
            return queryset.filter(Exists(models[name].objects.filter(
                user=self.request.user, recipe=OuterRef('id'))))
        return queryset

    def filter_tags(self, queryset, name, value):
        tags = self.data.getlist('tags')
        return queryset.filter(tags__slug__in=tags) if tags else queryset
