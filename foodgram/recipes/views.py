from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import AllowAny, IsAuthenticated

from recipes.models import (
    Favorites, Recipe, RecipeIngredients, RecipeTags, ShoppingList
)
from recipes.permissions import IsAuthorOrAdmin
from recipes.serializers import (
    RecipesGetSerializer, RecipesPostPatchSerializer
)
from tags.models import Tag


class RecipesViewSet(viewsets.ModelViewSet):
    """Работа с информацией о рецептах."""

    lookup_field = 'id'
    permission_classes = (IsAuthenticated, )
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
                    cur_tag = get_object_or_404(Tag, slug=tag)
                    ids = list(RecipeTags.objects.filter(tag=cur_tag).
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
