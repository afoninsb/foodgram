import base64

from django.core.files.base import ContentFile
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator
from rest_framework.fields import SerializerMethodField
from uuid import uuid1

from users.serializers import UserGetSerializer
from tags.serializers import TagSerializer
from ingredients.serializers import IngredientSerializer
from recipes.models import Favorites, Recipe, ShoppingList


class Base64ImageField(serializers.ImageField):
    def to_internal_value(self, data):
        if isinstance(data, str) and data.startswith("data:image"):
            format, imgstr = data.split(";base64,")
            ext = format.split("/")[-1]
            data = ContentFile(
                base64.b64decode(imgstr), name=f"{uuid1()}.{ext}")
        return super().to_internal_value(data)


class RecipesSerializer(serializers.ModelSerializer):
    """Сериализатор модели Recipes."""

    ingredients = IngredientSerializer(many=True, read_only=True)
    tags = TagSerializer(many=True, read_only=True)
    author = UserGetSerializer(read_only=True)
    image = serializers.CharField(source="image.url")

    class Meta:
        model = Recipe
        exclude = ("pub_date",)


class RecipesPostPatchSerializer(RecipesSerializer):
    """POST PATCH Сериализатор модели Recipes."""

    image = Base64ImageField()


class RecipesGetSerializer(RecipesSerializer):
    """GET Сериализатор модели Recipes."""

    def is_in_favorites(self, instance):
        user_id = self.context["request"].user.id
        recipe_id = instance.id
        try:
            return Favorites.objects.\
                filter(user_id=user_id, recipe_id=recipe_id).exists()
        except Exception:
            return False

    def is_in_shopping_list(self, instance):
        user_id = self.context["request"].user.id
        recipe_id = instance.id
        try:
            return ShoppingList.objects.\
                filter(user_id=user_id, recipe_id=recipe_id).exists()
        except Exception:
            return False

    is_favorited = SerializerMethodField(method_name="is_in_favorites")
    is_in_shopping_cart = SerializerMethodField(
        method_name="is_in_shopping_list")


class FavoriteRecipeSerializer(serializers.ModelSerializer):
    """Сериализатор модели Recipes для вывода в Избранное."""

    name = serializers.CharField(read_only=True)
    image = serializers.CharField(source="image.url", read_only=True)
    cooking_time = serializers.IntegerField(read_only=True)

    class Meta:
        model = Recipe
        fields = ("id", "name", "image", "cooking_time")


class FavoriteSerializer(serializers.ModelSerializer):
    """Сериализатор модели Favorites."""

    recipe = FavoriteRecipeSerializer(read_only=True)

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        return ret['recipe']

    class Meta:
        model = Favorites
        fields = ('recipe', )
