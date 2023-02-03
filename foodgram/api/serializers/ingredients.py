from ingredients.models import Ingredient
from rest_framework import serializers


class IngredientSerializer(serializers.ModelSerializer):
    """Сериализатор модели Ingredient."""

    class Meta:
        model = Ingredient
        fields = '__all__'
