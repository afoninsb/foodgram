from rest_framework import viewsets

from api.serializers.ingredients import IngredientSerializer
from ingredients.models import Ingredient


class IngredientsViewSet(viewsets.ReadOnlyModelViewSet):
    """Работа с информацией об ингредиентах."""

    serializer_class = IngredientSerializer

    def get_queryset(self):
        queryset = Ingredient.objects.all()
        if name := self.request.GET.get('name'):
            queryset = queryset.filter(name__startswith=name)
        return queryset
