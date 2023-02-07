from django.shortcuts import get_object_or_404
from djoser.serializers import SetPasswordSerializer
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from api.classesviewset import CreateListRetrieveViewSet
from api.pagination import Pagination
from api.serializers.users import (SubscriptionsSerializer,
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
            return SubscriptionsSerializer
        if self.action == 'set_password':
            return SetPasswordSerializer
        return UserGetSerializer

    def get_permissions(self):
        """Права доступа для запросов."""

        if self.action not in ('create', 'list', 'delete_subscribe'):
            self.permission_classes = (IsAuthenticated, )
        return super().get_permissions()

    @action(detail=False, methods=('GET',))
    def me(self, request):
        """Информация юзера о себе."""

        instance = request.user
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    @action(detail=False, methods=('POST',))
    def set_password(self, request):
        """Изменение пароля юзера."""

        serializer = self.get_serializer(
            data=request.data,
        )
        serializer.is_valid(raise_exception=True)
        self.request.user.set_password(request.data['new_password'])
        self.request.user.save()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=True, methods=('POST',))
    def subscribe(self, request, pk):
        """Подписка."""

        serializer = self.get_serializer(data={'id': pk})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    @subscribe.mapping.delete
    def delete_subscribe(self, request, pk):
        """Отмена подписки."""

        author = get_object_or_404(User, id=pk)
        if not Subscription.objects.filter(
            subscriber=request.user,
            author=author
        ).exists():
            return Response(
                'Вы не были подписаны',
                status=status.HTTP_400_BAD_REQUEST
            )
        Subscription.objects.get(
            subscriber=request.user,
            author=author
        ).delete()
        return Response

    @action(detail=False, methods=('GET',))
    def subscriptions(self, request):
        """Список подписок пользователя."""

        authors = Subscription.objects.filter(subscriber=request.user)
        page = self.paginate_queryset(authors)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(authors, many=True)
        return Response(serializer.data)
