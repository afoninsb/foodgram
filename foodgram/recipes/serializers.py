import base64
from uuid import uuid1

from django.core.files.base import ContentFile
from django.db.models import F
from django.shortcuts import get_object_or_404
from rest_framework import serializers
from rest_framework.fields import SerializerMethodField

from api.generic_serializer import RecipeUserListSerializer
from ingredients.models import Ingredient
from recipes.models import Favorites, Recipe, RecipeIngredients, ShoppingCart
from tags.models import Tag
from tags.serializers import TagSerializer
from users.serializers import UserGetSerializer


class Base64ImageField(serializers.ImageField):
    def to_internal_value(self, data):
        if isinstance(data, str) and data.startswith('data:image'):
            format, imgstr = data.split(';base64,')
            ext = format.split('/')[-1]
            data = ContentFile(
                base64.b64decode(imgstr), name=f'{uuid1()}.{ext}')
        return super().to_internal_value(data)


class RecipesSerializer(serializers.ModelSerializer):
    """Сериализатор модели Recipes."""

    ingredients = SerializerMethodField(method_name='get_ingredients')
    tags = TagSerializer(many=True, read_only=True)
    author = UserGetSerializer(read_only=True)
    is_favorited = serializers.BooleanField(read_only=True, default=False)
    is_in_shopping_cart = serializers.BooleanField(
        read_only=True, default=False)

    class Meta:
        model = Recipe
        fields = (
            'id', 'tags', 'author', 'ingredients', 'is_favorited',
            'is_in_shopping_cart', 'name', 'image', 'text', 'cooking_time'
        )

    def get_ingredients(self, instance):
        return instance.ingredients.annotate(
            amount=F('recipe_ingrdient__amount')).values(
                'id', 'name', 'measurement_unit', 'amount')


class TagsPrimaryKeyRelatedField(serializers.PrimaryKeyRelatedField):
    """Представление тэгов в списке рецептов."""

    def to_representation(self, value):
        serializer = TagSerializer(value)
        return serializer.data


class CreateRecipeIngredientSerializer(serializers.ModelSerializer):
    """Сериализатор модели ингредиентов рецепта."""

    id = serializers.IntegerField(write_only=True)
    amount = serializers.IntegerField(write_only=True)

    class Meta:
        model = RecipeIngredients
        fields = ('id', 'amount')

    def to_representation(self, value):
        for obj in self.context['request'].data['ingredients']:
            if obj['id'] == value.id:
                amount = obj['amount']
                break
        return {
            'id': value.id,
            'name': value.name,
            'measurement_unit': value.measurement_unit,
            'amount': amount,
        }


class RecipesPostPatchSerializer(RecipesSerializer):
    """POST PATCH Сериализатор модели Recipes."""

    tags = TagsPrimaryKeyRelatedField(
        queryset=Tag.objects.all(),
        many=True
    )
    ingredients = CreateRecipeIngredientSerializer(many=True)
    image = Base64ImageField()

    def create(self, validated_data):
        tags = validated_data.pop('tags')
        ingredients = validated_data.pop('ingredients')
        recipe = Recipe.objects.create(
            author=self.context['request'].user,
            **validated_data
        )
        recipe.tags.set(tags)
        self.SaveRecipeIngredients(recipe, ingredients)
        return recipe

    def update(self, instance, validated_data):
        tags = validated_data.pop('tags')
        ingredients = validated_data.pop('ingredients')
        instance = super().update(instance, validated_data)
        instance.tags.clear()
        instance.tags.set(tags)
        RecipeIngredients.objects.filter(recipe=instance).delete()
        self.SaveRecipeIngredients(instance, ingredients)
        return instance

    def SaveRecipeIngredients(self, recipe, ingredients):
        RecipeIngredients.objects.bulk_create([
            RecipeIngredients(
                recipe=recipe,
                ingredient=Ingredient.objects.get(id=ingredient['id']),
                amount=ingredient['amount']
            ) for ingredient in ingredients
        ])

    def validate_ingredients(self, data):
        for ingredient in data:
            try:
                get_object_or_404(Ingredient, id=ingredient['id'])
            except Exception as e:
                raise serializers.ValidationError(
                    f'Такого ингредиента нет - {ingredient["id"]}') from e
        return data


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
        user = self.context['request'].user
        recipe = get_object_or_404(Recipe, id=self.initial_data['id'])
        if self.model.objects.filter(user=user, recipe=recipe).exists():
            raise serializers.ValidationError("рецепт уже в этом списке")
        return {'user': user, 'recipe': recipe}

    def to_representation(self, instance):
        rep = super().to_representation({'recipe': instance.recipe})
        return rep['recipe']


class RecipesFavoriteSerializer(RecipesShoppingCartSerializer):
    """Сериализатор модели Favorites."""

    model = Favorites
