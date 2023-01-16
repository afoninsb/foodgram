from django.conf import settings
from djoser.serializers import UserCreateSerializer
from rest_framework import serializers

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

    def get_is_subscribed(self, obj):
        request_user = self.context.get('request').user.id
        return Subscription.objects.filter(
            subscriber=request_user,
            author=obj.id,
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
