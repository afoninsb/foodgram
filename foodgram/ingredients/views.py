from rest_framework import filters
from rest_framework.permissions import AllowAny

from foodgram.classesviewset import ListRetrieveViewSet
from ingredients.models import Ingredient
from ingredients.serializers import IngredientSerializer


class IngredientsViewSet(ListRetrieveViewSet):
    """Работа с информацией об ингредиентах."""

    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    lookup_field = 'id'
    filter_backends = [filters.SearchFilter]
    search_fields = ('^name',)
    permission_classes = (AllowAny, )
