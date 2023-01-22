from rest_framework import serializers

from recipes.models import Recipe


class FavoriteRecipeSerializer(serializers.ModelSerializer):
    '''Сериализатор модели Recipes для вывода в Избранное.'''

    name = serializers.CharField(read_only=True)
    image = serializers.CharField(source='image.url', read_only=True)
    cooking_time = serializers.IntegerField(read_only=True)

    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time')
