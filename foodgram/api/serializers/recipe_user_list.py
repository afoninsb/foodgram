from rest_framework import serializers

from recipes.models import Recipe


class RecipeUserListSerializer(serializers.ModelSerializer):
    """Сериализатор модели Recipes для вывода в списки рецептов."""

    name = serializers.CharField(read_only=True)
    cooking_time = serializers.IntegerField(read_only=True)
    image = serializers.ImageField(use_url=True)

    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time')
