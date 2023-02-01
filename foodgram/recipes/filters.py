from django.db.models import Exists, OuterRef
from django_filters import rest_framework as filters

from recipes.models import Favorites, Recipe, ShoppingCart


class RecipeFilter(filters.FilterSet):

    is_favorited = filters.BooleanFilter(method='filter_bool')
    is_in_shopping_cart = filters.BooleanFilter(method='filter_bool')
    author = filters.CharFilter()
    tags = filters.AllValuesMultipleFilter(field_name='tags__slug')

    class Meta:
        model = Recipe
        fields = ('is_favorited', 'is_in_shopping_cart', 'author', 'tags')

    def filter_bool(self, queryset, name, value):
        models = {
            'is_favorited': Favorites,
            'is_in_shopping_cart': ShoppingCart,
        }
        if self.request.user.is_authenticated and value == 1:
            return queryset.filter(Exists(models[name].objects.filter(
                user=self.request.user, recipe=OuterRef('id'))))
        return queryset
