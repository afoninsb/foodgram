from api.classesviewset import ListRetrieveViewSet
from ingredients.models import Ingredient
from ingredients.serializers import IngredientSerializer
from rest_framework import filters
from rest_framework.permissions import AllowAny


class IngredientsViewSet(ListRetrieveViewSet):
    """Работа с информацией об ингредиентах."""

    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ('^name',)
    permission_classes = (AllowAny,)
