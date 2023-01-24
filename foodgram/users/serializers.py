from django.conf import settings
from djoser.serializers import UserCreateSerializer
from rest_framework import serializers

from foodgram.generic_serializer import FavoriteRecipeSerializer
from users.models import Subscription, User


class UserPostSerializer(UserCreateSerializer):
    """POST Сериализатор модели User."""

    class Meta:
        model = User
        fields = ('email', 'username', 'first_name', 'last_name', 'password')

    def validate_username(self, value):
        """Проверяем, что username не равен me."""

        if value.lower() == settings.UNUSED_USERNAME:
            raise serializers.ValidationError(
                f'Username не может быть {settings.UNUSED_USERNAME}'
            )
        return value


class UserGetSerializer(serializers.ModelSerializer):
    """GET Сериализатор модели User."""

    is_subscribed = serializers.SerializerMethodField()
    email = serializers.CharField(read_only=True)
    username = serializers.CharField(read_only=True)
    first_name = serializers.CharField(read_only=True)
    last_name = serializers.CharField(read_only=True)

    def get_is_subscribed(self, obj):
        subscriber = self.context.get('request').user.id
        return Subscription.objects.filter(
            subscriber_id=subscriber,
            author=obj,
        ).exists()

    class Meta:
        model = User
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'is_subscribed'
        )


class UserGetSubSerializer(UserGetSerializer):
    """GET Сериализатор модели User для страницы подписок."""

    recipes = serializers.SerializerMethodField()
    recipes_count = serializers.SerializerMethodField()

    def get_recipes_count(self, obj):
        """Количество рецептов."""

        author = obj if self.context.get('request') else obj['author']
        return author.recipe.all().count()

    def get_recipes(self, obj):
        """Рецепты."""

        recipies = obj.recipe.all()
        if self.context.get('request').GET['recipes_limit']:
            count = int(self.context.get('request').GET['recipes_limit'])
            recipies = recipies[:count]
        return FavoriteRecipeSerializer(recipies, many=True).data

    class Meta:
        model = User
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'is_subscribed',
            'recipes',
            'recipes_count'
        )


class SubscriptionsListSerializer(serializers.ModelSerializer):
    """GET Сериализатор списка подписок."""

    author = UserGetSubSerializer(read_only=True)

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        return ret['author']

    class Meta:
        model = Subscription
        fields = ('author', )
