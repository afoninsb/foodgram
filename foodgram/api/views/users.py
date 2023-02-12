from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from api.classesviewset import CreateListRetrieveViewSet
from api.pagination import Pagination
from api.serializers.users import (SubscriptionListSerializer,
                                   SubscriptionSerializer,
                                   UserGetSerializer,
                                   UserPostSerializer)
from users.models import Subscription, User


class UsersViewSet(CreateListRetrieveViewSet):
    """Работа с информацией о пользователях."""

    queryset = User.objects.all()
    pagination_class = Pagination

    def get_serializer_class(self):
        """Выбор сериализатора."""

        if self.action == 'create':
            return UserPostSerializer
        if self.action in ('subscribe', 'subscriptions'):
            return SubscriptionSerializer
        return UserGetSerializer

    def get_permissions(self):
        """Права доступа для запросов."""

        if self.action not in ('create', 'list'):
            self.permission_classes = (IsAuthenticated, )
        return super().get_permissions()

    @action(detail=True, methods=('POST',))
    def subscribe(self, request, pk):
        """Подписка."""

        serializer = self.get_serializer(
            data={'id': pk},
            context={'request': self.request}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @subscribe.mapping.delete
    def delete_subscribe(self, request, pk):
        """Отмена подписки."""

        author = get_object_or_404(User, id=pk)
        obj = Subscription.objects.filter(
            subscriber=request.user,
            author=author
        )
        if obj.exists():
            obj.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(
            'Вы не были подписаны',
            status=status.HTTP_400_BAD_REQUEST
        )

    @action(detail=False, methods=('GET',))
    def subscriptions(self, request):
        """Список подписок пользователя."""

        authors = Subscription.objects.filter(
            subscriber=request.user).order_by('id')
        queryset = self.paginate_queryset(authors)
        serializer = SubscriptionListSerializer(
            queryset, context={'request': self.request}, many=True
        )
        return self.get_paginated_response(serializer.data)
