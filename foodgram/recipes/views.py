from django.db import IntegrityError
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from foodgram.generic_serializer import FavoriteRecipeSerializer

from recipes.models import (
    Favorites, Recipe, RecipeIngredients, RecipeTags, ShoppingList
)
from recipes.permissions import IsAuthorOrAdmin
from recipes.serializers import (
    RecipesGetSerializer, RecipesPostPatchSerializer
)


class RecipesViewSet(viewsets.ModelViewSet):
    """Работа с информацией о рецептах."""

    lookup_field = 'id'
    pagination_class = LimitOffsetPagination

    def get_permissions(self):
        """Права доступа для запросов."""

        if self.action == 'create':
            self.permission_classes = (IsAuthenticated, )
        elif self.action in ('partial_update', 'destroy'):
            self.permission_classes = (IsAuthorOrAdmin, )
        else:
            self.permission_classes = (AllowAny, )
        return super().get_permissions()

    def get_serializer_class(self):
        """Выбор серриализатора для чтения или записи."""

        if self.action in ('create', 'partial_update'):
            return RecipesPostPatchSerializer
        elif self.action in ('retrieve', 'list'):
            return RecipesGetSerializer
        elif self.action == 'favorite':
            return FavoriteRecipeSerializer

    def get_queryset(self):
        queryset = Recipe.objects.all()
        if self.request.GET:
            models = {
                'is_in_shopping_cart': ShoppingList,
                'is_favorited': Favorites
            }
            user_id = self.request.user.id
            for param, model in models.items():
                if (self.request.GET.get(param)
                        and self.request.GET.get(param) == '1'):
                    ids = list(model.objects.filter(user_id=user_id).
                               values_list('recipe_id', flat=True))
                    queryset = queryset.filter(id__in=ids)
            if self.request.GET.getlist('tags'):
                for tag in self.request.GET.getlist('tags'):
                    ids = list(RecipeTags.objects.filter(tag_id=tag).
                               values_list('recipe_id', flat=True))
                    queryset = queryset.filter(id__in=ids)
        return queryset

    def perform_create(self, serializer):
        data = serializer.validated_data
        recipe = serializer.save(
            author=self.request.user,
            image=data['image'],
            name=data['name'],
            text=data['text'],
            cooking_time=data['cooking_time'],
        )
        bulk_data = [
            RecipeIngredients(
                recipe=recipe,
                ingredient_id=ingredient['id'],
                amount=ingredient['amount'],
            )
            for ingredient in self.request.data['ingredients']
        ]
        RecipeIngredients.objects.bulk_create(bulk_data)
        bulk_data = [
            RecipeTags(recipe=recipe, tag_id=tag)
            for tag in self.request.data['tags']
        ]
        RecipeTags.objects.bulk_create(bulk_data)

    @action(detail=True, methods=('POST', 'DELETE'), url_path='favorite')
    def favorite(self, request, **kwargs):
        """Action subscribe - подписка и отмена подписки."""

        user = request.user
        recipe = get_object_or_404(Recipe, id=self.kwargs.get('id'))
        if request.method == 'POST':
            try:
                Favorites.objects.create(
                    user=user,
                    recipe=recipe
                )
            except IntegrityError:
                return Response(
                    'Этот рецепт уже в Избранном',
                    status=status.HTTP_400_BAD_REQUEST)
            else:
                serializer = FavoriteRecipeSerializer(
                    recipe,
                    data=request.data,
                )
                serializer.is_valid(raise_exception=True)
                return Response(
                    serializer.data,
                    status=status.HTTP_201_CREATED,
                )
        try:
            obj = get_object_or_404(Favorites, user=user, recipe=recipe)
        except Exception:
            return Response(
                'Этого рецепта нет в Избранном',
                status=status.HTTP_400_BAD_REQUEST
            )
        else:
            obj.delete()
            return Response(
                'Вы удалили рецепт из Избранного',
                status=status.HTTP_204_NO_CONTENT
            )
