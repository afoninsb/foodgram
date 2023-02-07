from django.conf import settings
from django.shortcuts import get_object_or_404
from djoser.serializers import UserCreateSerializer
from rest_framework import serializers

from api.serializers.recipe_user_list import RecipeUserListSerializer
from users.models import Subscription, User


class UserPostSerializer(UserCreateSerializer):
    """POST Сериализатор модели User."""

    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'password'
        )

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

    def get_is_subscribed(self, obj):
        subscriber = self.context.get('request').user.id
        return Subscription.objects.filter(
            subscriber_id=subscriber,
            author=obj,
        ).exists()


class UserGetSubSerializer(UserGetSerializer):
    """GET Сериализатор модели User для страницы подписок."""

    recipes = serializers.SerializerMethodField()
    recipes_count = serializers.SerializerMethodField()

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

    def get_recipes_count(self, obj):
        """Количество рецептов."""

        author = obj if self.context.get('request') else obj['author']
        return author.recipes.all().count()

    def get_recipes(self, obj):
        """Рецепты."""

        recipies = obj.recipes.all()
        if self.context.get('request').GET['recipes_limit']:
            count = int(self.context.get('request').GET['recipes_limit'])
            recipies = recipies[:count]
        return RecipeUserListSerializer(recipies, many=True).data


class SubscriptionsSerializer(serializers.ModelSerializer):
    """Сериализатор списка подписок."""

    author = UserGetSubSerializer(read_only=True)
    subscriber = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Subscription
        fields = ('author', 'subscriber')

    def create(self, validated_data):
        return Subscription.objects.create(**validated_data)

    def validate(self, data):
        subscriber = self.context['request'].user
        author = get_object_or_404(User, id=self.initial_data['id'])
        if subscriber == author:
            raise serializers.ValidationError("Нельзя подписаться на себя")
        if Subscription.objects.filter(
            subscriber=subscriber,
            author=author
        ).exists():
            raise serializers.ValidationError(
                "Вы уже подписаны на этого пользователя")
        return {'subscriber': subscriber, 'author': author}

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        return rep['author']
