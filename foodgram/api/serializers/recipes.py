import base64
from uuid import uuid1

from django.core.files.base import ContentFile
from django.db import transaction
from django.shortcuts import get_object_or_404
from rest_framework import serializers

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

    id = serializers.PrimaryKeyRelatedField(queryset=Ingredient.objects.all())
    name = serializers.CharField(source='ingredient.name', read_only=True)
    measurement_unit = serializers.CharField(
        source='ingredient.measurement_unit', read_only=True
    )

    class Meta:
        model = RecipeIngredient
        fields = ('id', 'name', 'measurement_unit', 'amount')


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
    is_favorited = serializers.BooleanField(default=False)
    is_in_shopping_cart = serializers.BooleanField(default=False)
    image = serializers.ImageField(use_url=True)

    class Meta:
        model = Recipe
        fields = (
            'id', 'tags', 'author', 'ingredients', 'is_favorited',
            'is_in_shopping_cart', 'name', 'image', 'text', 'cooking_time'
        )
        read_only_fields = ('author', 'is_favorited', 'is_in_shopping_cart')

    @transaction.atomic
    def create(self, validated_data):
        ingredients = validated_data.pop('recipe_ingrdient')
        tags = validated_data.pop('tags')
        recipe = Recipe.objects.create(
            author=self.context['request'].user,
            **validated_data
        )
        recipe.tags.set(tags)
        self.save_ingredients(recipe, ingredients)
        return recipe

    @transaction.atomic
    def update(self, instance, validated_data):
        ingredients = validated_data.pop('recipe_ingrdient')
        tags = validated_data.pop('tags')
        instance = super().update(instance, validated_data)
        instance.tags.clear()
        RecipeIngredient.objects.filter(recipe=instance).delete()
        instance.tags.set(tags)
        self.save_ingredients(instance, ingredients)
        return instance

    def save_ingredients(self, recipe, ingredients):
        RecipeIngredient.objects.bulk_create([
            RecipeIngredient(
                recipe=recipe,
                ingredient=ingredient['id'],
                amount=ingredient['amount'],
            )
            for ingredient in ingredients
        ])


class RecipesPostPatchSerializer(RecipesSerializer):
    """POST PATCH Сериализатор модели Recipes."""

    image = Base64ImageField()


class RecipeListsSerializer(serializers.ModelSerializer):
    """Вывод списка рецептов Избранное и Корзина."""

    image = serializers.ImageField(use_url=True)

    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time')
        read_only_fields = ('id', 'name', 'image', 'cooking_time')


class ShoppingCartSerializer(serializers.ModelSerializer):
    """Список рецептов в Корзине."""

    class Meta:
        model = ShoppingCart
        fields = ('user', 'recipe')

    def validate(self, data):
        recipe = data['recipe']
        if ShoppingCart.objects.filter(
                user=data['user'],
                recipe=recipe,
        ).exists():
            raise serializers.ValidationError(
                f'Рецепт `{recipe.name}` уже в корзине'
            )
        return data

    def to_representation(self, instance: ShoppingCart):
        return RecipeListsSerializer(
            instance.recipe,
            context={'request': self.context['request']}
        ).data


class FavoriteSerializer(serializers.ModelSerializer):
    """Список рецептов в Избранном."""

    class Meta:
        model = Favorite
        fields = ('user', 'recipe')

    def validate(self, attrs):
        recipe = attrs['recipe']
        if Favorite.objects.filter(
                user=attrs['user'],
                recipe=recipe,
        ).exists():
            raise serializers.ValidationError(
                f'Рецепт `{recipe.name}` уже в избранных'
            )
        return attrs

    def to_representation(self, instance: Favorite):
        return RecipeListsSerializer(
            instance.recipe,
            context={'request': self.context['request']}
        ).data
