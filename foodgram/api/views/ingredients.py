from rest_framework import filters, viewsets

from api.serializers.ingredients import IngredientSerializer
from ingredients.models import Ingredient


class IngredientsViewSet(viewsets.ReadOnlyModelViewSet):
    """Работа с информацией об ингредиентах."""

    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ('^name',)
