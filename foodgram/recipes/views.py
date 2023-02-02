from api.pagination import RecipePagination
from django.db.models import Exists, OuterRef
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.template.loader import render_to_string
from django_filters.rest_framework import DjangoFilterBackend
from recipes.filters import RecipeFilter
from recipes.models import Favorites, Recipe, ShoppingCart
from recipes.permissions import IsAuthor
from recipes.serializers import (RecipesFavoriteSerializer,
                                 RecipesPostPatchSerializer, RecipesSerializer,
                                 RecipesShoppingCartSerializer)
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from weasyprint import HTML


class RecipesViewSet(viewsets.ModelViewSet):
    """Работа с информацией о рецептах."""

    queryset = Recipe.objects.all()
    http_method_names = ('get', 'post', 'patch', 'delete')
    pagination_class = RecipePagination
    filter_backends = (DjangoFilterBackend,)
    filterset_class = RecipeFilter
    template = 'shopping_cart.html'
    filename = "shopping_cart.pdf"

    def get_permissions(self):
        """Права доступа для запросов."""

        if self.action in ('retrieve', 'list'):
            self.permission_classes = (AllowAny, )
        elif self.action in ('partial_update', 'destroy'):
            self.permission_classes = (IsAuthor,)
        else:
            self.permission_classes = (IsAuthenticated, )
        return super().get_permissions()

    def get_serializer_class(self):
        """Выбор сериализатора для чтения или записи."""

        if self.action in ('create', 'partial_update'):
            return RecipesPostPatchSerializer
        if self.action in ('retrieve', 'list'):
            return RecipesSerializer
        if self.action == 'favorite':
            return RecipesFavoriteSerializer
        if self.action == 'shopping_cart':
            return RecipesShoppingCartSerializer

    def get_queryset(self):
        """Получаем queryset рецептов."""

        if self.request.user.is_authenticated:
            return Recipe.objects.annotate(
                is_favorited=Exists(Favorites.objects.filter(
                    user=self.request.user, recipe=OuterRef('id'))),
                is_in_shopping_cart=Exists(ShoppingCart.objects.filter(
                    user=self.request.user, recipe=OuterRef('id')))
            ).select_related('author').prefetch_related(
                'tags', 'ingredients')
        return Recipe.objects.select_related('author').prefetch_related(
                'tags', 'ingredients')

    @action(detail=True, methods=('POST',))
    def favorite(self, request, pk):
        """Добавление в Избранное."""

        return self.user_lists(request, pk)

    @favorite.mapping.delete
    def delete_favorite(self, request, pk):
        """Удаление из Избранного."""

        return self.del_user_lists(request, Favorites, pk)

    @action(detail=True, methods=('POST',))
    def shopping_cart(self, request, pk):
        """Добавление в Список покупок."""

        return self.user_lists(request, pk)

    @shopping_cart.mapping.delete
    def delete_shopping_cart(self, request, pk):
        """Удаление из Списка покупок."""

        return self.del_user_lists(request, ShoppingCart, pk)

    def user_lists(self, request, pk):
        """Добавление в списки Избранное и Покупок."""

        if request.method == 'POST':
            serializer = self.get_serializer(data={'id': pk})
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)

    def del_user_lists(self, request, model, pk):
        """Удаление из списков Избранное и Покупок."""

        obj = get_object_or_404(
            model,
            user=request.user,
            recipe_id=pk
        )
        obj.delete()
        return Response(
            'Вы удалили рецепт из списка',
            status=status.HTTP_204_NO_CONTENT
        )

    @action(detail=False, methods=('GET', ))
    def download_shopping_cart(self, request, **kwargs):
        """Получение документа со списком ингредиентов для покупки."""

        spisok = Recipe.objects.filter(
            Exists(ShoppingCart.objects.filter(
                user=request.user, recipe=OuterRef('id'))
            )
        ).prefetch_related('recipe_ingrdient')
        info = {'ingredients': {}, 'recipes': {}}
        for recipe in spisok:
            info['recipes'][recipe.name] = []
            for ingredient in recipe.recipe_ingrdient.all():
                obj = ingredient.ingredient
                info['recipes'][recipe.name].append(obj.name)
                if not info['ingredients'].get(obj.name):
                    info['ingredients'][obj.name] = [
                        ingredient.amount,
                        obj.measurement_unit
                    ]
                else:
                    info['ingredients'][obj.name][0] += ingredient.amount

        html_template = render_to_string(
            self.template, {'info': info})
        pdf_file = HTML(string=html_template).write_pdf()
        response = HttpResponse(pdf_file, content_type='application/pdf')
        response['Content-Disposition'] = f'filename={self.filename}'
        return response
