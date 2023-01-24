from django.db import IntegrityError
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response

from foodgram.classesviewset import CreateListRetrieveViewSet, ListViewSet
from foodgram.pagination import MyPagination
from users.models import Subscription, User
from users.serializers import (
    SubscriptionsListSerializer,
    UserGetSerializer,
    UserGetSubSerializer,
    UserPostSerializer
)


class UsersViewSet(CreateListRetrieveViewSet):
    """Работа с информацией о пользователях."""

    queryset = User.objects.all()
    lookup_field = 'id'
    pagination_class = MyPagination

    def get_serializer_class(self):
        """Выбор сериализатора."""

        if self.action == 'create':
            return UserPostSerializer
        elif self.action == 'subscribe':
            return UserGetSubSerializer
        else:
            return UserGetSerializer

    def get_permissions(self):
        """Права доступа для GET запросов."""

        if self.action in ('retrieve', 'me', 'set_password', 'subscribe'):
            self.permission_classes = (IsAuthenticated, )
        else:
            self.permission_classes = (AllowAny, )
        return super().get_permissions()

    def create(self, request, *args, **kwargs):
        """Метод create модели User."""

        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            self.perform_create(serializer)
            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=('GET',), url_path='me')
    def me(self, request):
        """Информация юзера о себе."""

        instance = request.user
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    @action(detail=False, methods=('POST',), url_path='set_password')
    def set_password(self, request):
        """Изменение пароля юзера."""

        instance = request.user
        serializer = self.get_serializer(
            instance,
            request.data,
            partial=True
        )
        if serializer.is_valid(raise_exception=True):
            self.request.user.set_password(request.data['new_password'])
            self.request.user.save()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=('POST', 'DELETE'), url_path='subscribe')
    def subscribe(self, request, **kwargs):
        """Action subscribe - подписка и отмена подписки."""

        subscriber = request.user
        author = get_object_or_404(User, id=self.kwargs.get('id'))
        if request.method == 'POST':
            try:
                Subscription.objects.create(
                    subscriber=subscriber,
                    author=author
                )
            except IntegrityError:
                return Response(
                    'Вы уже подписаны на этого пользователя',
                    status=status.HTTP_400_BAD_REQUEST)
            else:
                serializer = self.get_serializer(
                    author,
                    data=request.data,
                    context={'request': request}
                )
                serializer.is_valid(raise_exception=True)
                return Response(
                    serializer.data,
                    status=status.HTTP_201_CREATED,
                )
        try:
            obj = get_object_or_404(
                Subscription,
                subscriber=subscriber,
                author=author
            )
        except Exception:
            return Response(
                'Вы не подписаны на этого пользователя',
                status=status.HTTP_400_BAD_REQUEST)
        else:
            obj.delete()
            return Response(
                'Вы отписались от этого пользователя',
                status=status.HTTP_204_NO_CONTENT)


class GetSubscriptionsViewSet(ListViewSet):
    """Работа с информацией о подписках пользователя."""

    serializer_class = SubscriptionsListSerializer
    permission_classes = (IsAuthenticated, )
    pagination_class = LimitOffsetPagination

    def get_queryset(self):
        return Subscription.objects.filter(subscriber=self.request.user)
