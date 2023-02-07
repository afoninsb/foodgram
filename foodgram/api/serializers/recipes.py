import base64
from uuid import uuid1

from django.core.files.base import ContentFile
from django.db import transaction
from django.shortcuts import get_object_or_404
from rest_framework import serializers

from api.serializers.recipe_user_list import RecipeUserListSerializer
from api.serializers.users import UserGetSerializer
from ingredients.models import Ingredient
from recipes.models import Favorite, Recipe, RecipeIngredient, ShoppingCart
from tags.models import Tag


class Base64ImageField(serializers.ImageField):
    def to_internal_value(self, data):
        if isinstance(data, str) and data.startswith('data:image'):
            format, imgstr = data.split(';base64,')
            ext = format.split('/')[-1]
            data = ContentFile(
                base64.b64decode(imgstr), name=f'{uuid1()}.{ext}')
        return super().to_internal_value(data)


class RecipeIngredientsSerializer(serializers.ModelSerializer):
    """Сериализатор связи Recipe-Ingredients."""

    id = serializers.IntegerField(source='ingredient.id')
    name = serializers.CharField(source='ingredient.name', read_only=True)
    measurement_unit = serializers.CharField(
        source='ingredient.measurement_unit',
        read_only=True
    )
    amount = serializers.IntegerField()

    class Meta:
        model = RecipeIngredient
        fields = ('id', 'name', 'measurement_unit', 'amount')

    def validate_id(self, value):
        """Проверяем, что ингредиент существует."""

        get_object_or_404(Ingredient, id=value)
        return value


class RecipeTags(serializers.Field):
    """Класс поля тэгов."""

    def to_representation(self, value):
        return value.instance.tags.all().values()

    def to_internal_value(self, data):
        for tag_id in data:
            get_object_or_404(Tag, id=tag_id)
        return data


class RecipesSerializer(serializers.ModelSerializer):
    """Сериализатор модели Recipes."""

    ingredients = RecipeIngredientsSerializer(
        many=True,
        source='recipe_ingrdient'
    )
    tags = RecipeTags()
    author = UserGetSerializer(read_only=True)
    is_favorited = serializers.BooleanField(read_only=True, default=False)
    is_in_shopping_cart = serializers.BooleanField(
        read_only=True,
        default=False
    )
    image = serializers.ImageField(use_url=True)

    class Meta:
        model = Recipe
        fields = (
            'id', 'tags', 'author', 'ingredients', 'is_favorited',
            'is_in_shopping_cart', 'name', 'image', 'text', 'cooking_time'
        )

    @transaction.atomic
    def create(self, validated_data):
        _ = validated_data.pop('recipe_ingrdient')
        tags = validated_data.pop('tags')
        recipe = Recipe.objects.create(
            author=self.context['request'].user,
            **validated_data
        )
        recipe.tags.set(tags)
        self.save_ingredients(recipe)
        return recipe

    @transaction.atomic
    def update(self, instance, validated_data):
        _ = validated_data.pop('recipe_ingrdient')
        tags = validated_data.pop('tags')
        instance = super().update(instance, validated_data)
        instance.tags.clear()
        RecipeIngredient.objects.filter(recipe=instance).delete()
        instance.tags.set(tags)
        self.save_ingredients(instance)
        return instance

    def save_ingredients(self, recipe):
        ingredients = self.context['request'].data['ingredients']
        RecipeIngredient.objects.bulk_create([
            RecipeIngredient(
                recipe=recipe,
                ingredient_id=ingredient['id'],
                amount=ingredient['amount'],
            )
            for ingredient in ingredients
        ])


class RecipesPostPatchSerializer(RecipesSerializer):
    """POST PATCH Сериализатор модели Recipes."""

    image = Base64ImageField()


class RecipesShoppingCartSerializer(serializers.ModelSerializer):
    """Сериализатор модели ShoppingCart."""

    user = UserGetSerializer(read_only=True)
    recipe = RecipeUserListSerializer(read_only=True)
    model = ShoppingCart

    class Meta:
        model = ShoppingCart
        fields = ('recipe', 'user')

    def create(self, validated_data):
        return self.model.objects.create(**validated_data)

    def validate(self, data):
        recipe_id = self.initial_data['id']
        if not Recipe.objects.filter(id=recipe_id).exists():
            raise serializers.ValidationError(
                f"Такого рецепта нет - {recipe_id}"
            )
        user = self.context['request'].user
        if self.model.objects.filter(user=user, recipe_id=recipe_id).exists():
            raise serializers.ValidationError("Рецепт уже в этом списке")
        return {'user': user, 'recipe': Recipe.objects.get(id=recipe_id)}

    def to_representation(self, instance):
        rep = super().to_representation({'recipe': instance.recipe})
        return rep['recipe']


class RecipesFavoriteSerializer(RecipesShoppingCartSerializer):
    """Сериализатор модели Favorite."""

    model = Favorite
