# from api.v1.filters import TitleFilter
# from api.v1.permissions import (IsAdmin, IsAdminOrReadOnly,
#                                 IsAuthorModeratorAdminOrReadOnly)
# from api.v1.serializers import (CategorySerializer, CommentSerializer,
#                                 GenreSerializer, ReviewSerializer,
#                                 SignupSerializer, TitleReadSerializer,
#                                 TitleWriteSerializer, TokenSerializer,
#                                 UserSerializer)
# from django.conf import settings
# from django.contrib.auth.tokens import default_token_generator
# from django.core.mail import send_mail
# from django.db import IntegrityError
# from django.db.models import Avg
# from django.shortcuts import get_object_or_404
# from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, mixins, status, viewsets
from rest_framework.decorators import action, api_view
# from rest_framework.permissions import (IsAuthenticated,
#                                         IsAuthenticatedOrReadOnly)
# from rest_framework.response import Response
# from rest_framework_simplejwt.tokens import AccessToken
# from reviews.models import Category, Genre, Review, Title
# from users.models import User


@api_view(('POST',))
def signup(request):
    """
    Регистрация пользователя с отправкой кода подтверждения на почту.
    """
    pass
    # serializer = SignupSerializer(data=request.data)
    # serializer.is_valid(raise_exception=True)
    # username = serializer.validated_data['username']
    # email = serializer.validated_data['email']
    # try:
    #     user, _ = User.objects.get_or_create(
    #         username=username,
    #         email=email,
    #     )
    # except IntegrityError:
    #     return Response(
    #         'Такой пары username-email нет в базе данных',
    #         status=status.HTTP_400_BAD_REQUEST
    #     )

    # confirmation_code = default_token_generator.make_token(user)
    # send_mail(
    #     subject='confirmation_code',
    #     message=f'{username} - {confirmation_code}',
    #     from_email=settings.FROM,
    #     recipient_list=[email],
    #     fail_silently=False,
    # )
    # return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(('POST',))
def get_token(request):
    """
    Получение токена авторизации.
    """
    pass
    # serializer = TokenSerializer(data=request.data)
    # serializer.is_valid(raise_exception=True)
    # user = get_object_or_404(
    #     User, username=serializer.validated_data['username'])
    # confirmation_code = serializer.validated_data['confirmation_code']
    # if not default_token_generator.check_token(user, confirmation_code):
    #     return Response(
    #         'Передан некорректный код подтверждения',
    #         status=status.HTTP_400_BAD_REQUEST
    #     )
    # token = AccessToken.for_user(user)
    # return Response(
    #     {'token': str(token)},
    #     status=status.HTTP_200_OK
    # )


class UsersViewSet(viewsets.ModelViewSet):
    """
    Работа с информацией о пользователях.
    """
    pass
    # queryset = User.objects.all()
    # serializer_class = UserSerializer
    # permission_classes = (IsAdmin,)
    # search_fields = ('username',)
    # lookup_field = 'username'

    # @action(
    #     detail=False,
    #     methods=('get', 'patch'),
    #     url_path='me',
    #     permission_classes=(IsAuthenticated,)
    # )
    # def me(self, request):
    #     instance = request.user
    #     if request.method == 'GET':
    #         serializer = self.get_serializer(instance)
    #         return Response(serializer.data)
    #     serializer = self.get_serializer(
    #         instance,
    #         request.data,
    #         partial=True
    #     )
    #     serializer.is_valid(raise_exception=True)
    #     serializer.save(role=instance.role, partial=True)
    #     return Response(serializer.data)
