from rest_framework import filters

from foodgram.classesviewset import ListRetrieveViewSet
from ingredients.serializers import IngredientSerializer
from ingredients.models import Ingredient


class IngredientsViewSet(ListRetrieveViewSet):
    """Работа с информацией об ингредиентах."""

    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    lookup_field = 'id'
    filter_backends = [filters.SearchFilter]
    search_fields = ('^name',)
