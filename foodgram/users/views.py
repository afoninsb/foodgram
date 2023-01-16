from rest_framework import mixins, status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from users.models import User
from users.pagination import UserPagination
from users.serializers import UserGetSerializer, UserPostSerializer


class CreateListRetrieveViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet,
):
    pass


class UsersViewSet(CreateListRetrieveViewSet):
    """Работа с информацией о пользователях."""

    queryset = User.objects.all()
    search_fields = ('username',)
    lookup_field = 'id'
    pagination_class = UserPagination

    def get_serializer_class(self):
        """Выбор серриализатора для чтения или записи."""

        return (UserPostSerializer
                if self.action == 'create' else UserGetSerializer)

    def get_permissions(self):
        """Права доступа для GET запросов."""

        if self.action in ('create', 'list'):
            self.permission_classes = (AllowAny, )
        elif self.action in ('retrieve', 'me', 'set_password'):
            self.permission_classes = (IsAuthenticated, )
        return super().get_permissions()

    def create(self, request, *args, **kwargs):
        """Метод create модели User."""

        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED,
                headers=headers
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=('get',), url_path='me')
    def me(self, request):
        """Action me - информация юзера о себе."""

        instance = request.user
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    @action(detail=False, methods=('post',), url_path='set_password')
    def set_password(self, request):
        """Action set_password - изменение пароля юзера."""

        instance = request.user
        print(request.data)
        serializer = self.get_serializer(
            instance,
            request.data,
            partial=True
        )
        if serializer.is_valid(raise_exception=True):
            self.request.user.set_password(request.data["new_password"])
            self.request.user.save()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
