from django.db import IntegrityError
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.template.loader import render_to_string
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from weasyprint import HTML

from api.generic_serializer import FavoriteRecipeSerializer
from api.pagination import RecipePagination
from users.models import User
from recipes.models import (
    Favorites, Recipe, RecipeIngredients, ShoppingCart
)
from recipes.permissions import IsAuthor
from recipes.serializers import RecipesPostPatchSerializer, RecipesSerializer
from tags.models import Tag


class RecipesViewSet(viewsets.ModelViewSet):
    """Работа с информацией о рецептах."""

    http_method_names = ('get', 'post', 'patch', 'delete')
    pagination_class = RecipePagination

    def get_permissions(self):
        """Права доступа для запросов."""

        if self.action in ('retrieve', 'list'):
            self.permission_classes = (AllowAny, )
        elif self.action in ('partial_update', 'destroy'):
            self.permission_classes = (IsAuthor, )
        else:
            self.permission_classes = (IsAuthenticated, )
        return super().get_permissions()

    def get_serializer_class(self):
        """Выбор сериализатора для чтения или записи."""

        if self.action in ('create', 'partial_update'):
            return RecipesPostPatchSerializer
        if self.action in ('retrieve', 'list'):
            return RecipesSerializer
        if self.action in ('favorite', 'shopping_cart'):
            return FavoriteRecipeSerializer

    def get_queryset(self):
        queryset = Recipe.objects.all()
        if self.action == 'list':
            models = {
                'is_in_shopping_cart': ShoppingCart,
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
                ids = set()
                for tag_slug in self.request.GET.getlist('tags'):
                    tag = get_object_or_404(Tag, slug=tag_slug)
                    obj = set(tag.recipe_set.all().
                              values_list('id', flat=True))
                    ids |= obj
                queryset = queryset.filter(id__in=ids)
            if self.request.GET.get('author'):
                author = get_object_or_404(
                    User, id=self.request.GET.get('author')
                )
                ids = list(author.recipes.all().values_list('id', flat=True))
                queryset = queryset.filter(id__in=ids)
        return queryset

    @action(detail=True, methods=('POST', 'DELETE'))
    def favorite(self, request, **kwargs):
        """Добавление в Избранное и удаление из Избранного."""

        return self.user_lists(request, Favorites)

    @action(detail=True, methods=('POST', 'DELETE'))
    def shopping_cart(self, request, **kwargs):
        """Добавление в список покупок и удаление из него."""

        return self.user_lists(request, ShoppingCart)

    @action(detail=False, methods=('GET', ))
    def download_shopping_cart(self, request, **kwargs):
        """Получение документа со списком ингредиентов для покупки."""

        user = request.user
        spisok = ShoppingCart.objects.filter(user=user)
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
