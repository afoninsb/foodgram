from rest_framework import serializers

from recipes.models import Recipe


class RecipeUserListSerializer(serializers.ModelSerializer):
    """Сериализатор модели Recipes для вывода в Избранное."""

    name = serializers.CharField(read_only=True)
    cooking_time = serializers.IntegerField(read_only=True)

    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time')
