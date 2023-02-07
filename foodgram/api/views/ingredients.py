from rest_framework import viewsets

from api.serializers.ingredients import IngredientSerializer
from ingredients.models import Ingredient


class IngredientsViewSet(viewsets.ReadOnlyModelViewSet):
    """Работа с информацией об ингредиентах."""

    serializer_class = IngredientSerializer

    def get_queryset(self):
        if name := self.request.GET.get('name'):
            return Ingredient.objects.filter(name__startswith=name)
        return Ingredient.objects.all()
