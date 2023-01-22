from django.db import IntegrityError
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.template.loader import render_to_string
from rest_framework import status
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from foodgram.generic_serializer import FavoriteRecipeSerializer
from weasyprint import HTML

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
        elif self.action in ['favorite', 'shopping_cart']:
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
        """Добавление в Избранное и удаление из Избранного."""

        return self.user_lists(request, Favorites)

    @action(detail=True, methods=('POST', 'DELETE'), url_path='shopping_cart')
    def shopping_cart(self, request, **kwargs):
        """Добавление в список покупок и удаление из него."""

        return self.user_lists(request, ShoppingList)

    @action(detail=False, methods=('GET', ), url_path='download_shopping_cart')
    def download_shopping_cart(self, request, **kwargs):
        """Получение документа сос писком ингредиентов для покупки."""

        user = request.user
        spisok = ShoppingList.objects.filter(user=user)
        download = {}
        for obj in spisok:
            ingredients = RecipeIngredients.objects.\
                filter(recipe=obj.recipe).select_related('ingredient')
            for ingredient in ingredients:
                obj = ingredient.ingredient
                if obj.name in download:
                    download[obj.name][0] += ingredient.amount
                else:
                    download[obj.name] = (
                        [ingredient.amount, obj.measurement_unit]
                    )
        html_template = render_to_string(
            'shopping_cart.html', {'download': download})
        pdf_file = HTML(string=html_template).write_pdf()
        response = HttpResponse(pdf_file, content_type='application/pdf')
        response['Content-Disposition'] = 'filename="shopping_cart.pdf"'
        return response

    def user_lists(self, request, model):
        user = request.user
        recipe = get_object_or_404(Recipe, id=self.kwargs.get('id'))
        if request.method == 'POST':
            try:
                model.objects.create(
                    user=user,
                    recipe=recipe
                )
            except IntegrityError:
                return Response(
                    'Этот рецепт уже в списке',
                    status=status.HTTP_400_BAD_REQUEST)
            else:
                serializer = self.get_serializer(
                    recipe,
                    data=request.data,
                )
                serializer.is_valid(raise_exception=True)
                return Response(
                    serializer.data,
                    status=status.HTTP_201_CREATED,
                )
        try:
            obj = get_object_or_404(model, user=user, recipe=recipe)
        except Exception:
            return Response(
                'Этого рецепта нет в списке',
                status=status.HTTP_400_BAD_REQUEST
            )
        else:
            obj.delete()
            return Response(
                'Вы удалили рецепт из списка',
                status=status.HTTP_204_NO_CONTENT
            )
