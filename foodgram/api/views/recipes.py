from django.db.models import Exists, OuterRef
from django.http import HttpResponse
from django.template.loader import render_to_string
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from weasyprint import HTML

from api.filters import RecipeFilter
from api.pagination import Pagination
from api.permissions import IsAuthor
from api.serializers.recipes import (FavoriteSerializer,
                                     #RecipesFavoriteSerializer,
                                     RecipesPostPatchSerializer,
                                     RecipesSerializer,
                                     #RecipesShoppingCartSerializer,
                                     ShoppingCartSerializer)
from recipes.models import Favorite, Recipe, ShoppingCart


class RecipesViewSet(viewsets.ModelViewSet):
    """Работа с информацией о рецептах."""

    queryset = Recipe.objects.all()
    http_method_names = ('get', 'post', 'patch', 'delete')
    pagination_class = Pagination
    filter_backends = (DjangoFilterBackend,)
    filterset_class = RecipeFilter
    template = 'shopping_cart.html'
    filename = 'shopping_cart.pdf'

    def get_permissions(self):
        """Права доступа для запросов."""

        if self.action in (
            'create',
            'favorite',
            'shopping_cart',
            'download_shopping_cart',
            'delete_favorite',
            'delete_shopping_cart'
        ):
            self.permission_classes = (IsAuthenticated, )
        elif self.action in ('partial_update', 'destroy'):
            self.permission_classes = (IsAuthor,)
        return super().get_permissions()

    def get_serializer_class(self):
        """Выбор сериализатора для чтения или записи."""

        if self.action in ('create', 'partial_update'):
            return RecipesPostPatchSerializer
        if self.action == 'favorite':
            return RecipesFavoriteSerializer
        if self.action == 'shopping_cart':
            return RecipesShoppingCartSerializer
        return RecipesSerializer

    def get_queryset(self):
        """Получаем queryset рецептов."""

        if self.request.user.is_authenticated:
            return self.queryset.annotate(
                is_favorited=Exists(Favorite.objects.filter(
                    user=self.request.user, recipe=OuterRef('id'))),
                is_in_shopping_cart=Exists(ShoppingCart.objects.filter(
                    user=self.request.user, recipe=OuterRef('id')))
            ).select_related('author').prefetch_related(
                'tags', 'ingredients')
        return self.queryset.select_related(
            'author').prefetch_related('tags', 'ingredients')

    # @action(detail=True, methods=('POST',))
    # def favorite(self, request, pk):
    #     """Добавление в Избранное."""

    #     return self.user_lists(pk)

    @action(methods=('POST',), detail=True,
            serializer_class=FavoriteSerializer)
    def favorite(self, request, pk: int):
        serializer = FavoriteSerializer(
            data={'recipe': pk, 'user': self.request.user.id},
            context={'request': request},
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @favorite.mapping.delete
    def delete_favorite(self, request, pk):
        """Удаление из Избранного."""

        return self.del_user_lists(Favorite, pk)

    # @action(detail=True, methods=('POST',))
    # def shopping_cart(self, request, pk):
    #     """Добавление в Список покупок."""

    #     return self.user_lists(pk)

    @action(methods=('POST',), detail=True,
            serializer_class=ShoppingCartSerializer)
    def shopping_cart(self, request, pk: int):
        serializer = ShoppingCartSerializer(
            data={'recipe': pk, 'user': self.request.user.id},
            context={'request': request},
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @shopping_cart.mapping.delete
    def delete_shopping_cart(self, request, pk):
        """Удаление из Списка покупок."""

        return self.del_user_lists(ShoppingCart, pk)

    def user_lists(self, pk):
        """Добавление в списки Избранное и Покупок."""

        serializer = self.get_serializer(data={'id': pk})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def del_user_lists(self, model, pk):
        """Удаление из списков Избранное и Покупок."""

        if not model.objects.filter(
            user=self.request.user,
            recipe_id=pk
        ).exists():
            return Response(
                'Этого рецепта нет в списке',
                status=status.HTTP_400_BAD_REQUEST
            )
        model.objects.get(user=self.request.user, recipe_id=pk).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

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
