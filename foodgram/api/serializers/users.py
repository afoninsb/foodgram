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


class SubscriptionSerializer(UserGetSerializer):
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
            raise serializers.ValidationError('Нельзя подписаться на себя')
        if Subscription.objects.filter(
            subscriber=subscriber,
            author=author
        ).exists():
            raise serializers.ValidationError(
                'Вы уже подписаны на этого пользователя')
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

        return obj.recipes.count()

    def get_recipes(self, obj):
        """Рецепты."""

        recipes = obj.recipes.all()
        limit = self.context.get('request').GET.get('recipes_limit', '')
        if limit.isdigit():
            recipes = recipes[:int(limit)]
        return RecipeUserListSerializer(
            recipes,
            context={'request': self.context['request']},
            many=True
        ).data


class SubscriptionListSerializer(serializers.ModelSerializer):
    """Сериализатор списка подписок."""

    author = SubscriptionSerializer(read_only=True)
    subscriber = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Subscription
        fields = ('author', 'subscriber')

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        return rep['author']
