from rest_framework import filters
from rest_framework.permissions import AllowAny

from api.classesviewset import ListRetrieveViewSet
from api.serializers.ingredients import IngredientSerializer
from ingredients.models import Ingredient


class IngredientsViewSet(ListRetrieveViewSet):
    """Работа с информацией об ингредиентах."""

    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ('^name',)
    permission_classes = (AllowAny,)
