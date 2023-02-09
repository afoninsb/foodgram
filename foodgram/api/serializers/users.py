from django.conf import settings
from djoser.serializers import UserCreateSerializer
from rest_framework import serializers

from recipes.models import Recipe
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


class RecipeUserListSerializer(serializers.ModelSerializer):
    """Сериализатор модели Recipes для вывода в списки рецептов."""

    image = serializers.ImageField(use_url=True)

    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time')


class UserGetSerializer(serializers.ModelSerializer):
    """GET Сериализатор модели User."""

    is_subscribed = serializers.SerializerMethodField()
    # email = serializers.CharField(read_only=True)
    # username = serializers.CharField(read_only=True)
    # first_name = serializers.CharField(read_only=True)
    # last_name = serializers.CharField(read_only=True)

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
        read_only_fields = ('email', 'username', 'first_name', 'last_name')

    def get_is_subscribed(self, obj):
        subscriber = self.context.get('request').user
        return (
            Subscription.objects.filter(
                subscriber=subscriber,
                author=obj,
            ).exists()
            if subscriber.is_authenticated
            else False
        )


class SubscriptionsSerializer(UserGetSerializer):
    """Сериализатор списка подписок."""

    id = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
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
        read_only_fields = ('email', 'username', 'first_name', 'last_name')

    def validate(self, data):
        subscriber = self.context['request'].user
        author = data['id']
        if subscriber == author:
            raise serializers.ValidationError("Нельзя подписаться на себя")
        if Subscription.objects.filter(
            subscriber=subscriber,
            author=author
        ).exists():
            raise serializers.ValidationError(
                "Вы уже подписаны на этого пользователя")
        return data

    def create(self, validated_data):
        author = validated_data['id']
        Subscription.objects.create(
            subscriber=self.context['request'].user,
            author=author
        )
        return author

    def get_recipes_count(self, obj):
        """Количество рецептов."""

        return obj.recipes.all().count()

    def get_recipes(self, obj):
        """Рецепты."""

        recipes = obj.recipes.all()
        if self.context.get('request').GET.get('recipes_limit'):
            recipes = recipes[:int(self.context.get(
                'request').GET['recipes_limit'])]
        return RecipeUserListSerializer(recipes, many=True).data
