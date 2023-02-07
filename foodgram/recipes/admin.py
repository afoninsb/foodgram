from django.contrib import admin
from django.db.models import Count

from recipes.models import Favorite, Recipe, RecipeIngredient, ShoppingCart


class IngredientInline(admin.TabularInline):
    model = Recipe.ingredients.through
    min_num = 1


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    """Представление рецептов в админ-панели."""

    list_display = (
        'name',
        'author',
        'text',
        'cooking_time',
        'image',
        'count_favorite',
    )
    list_filter = ('tags', 'name', 'author')
    search_fields = ('name',)
    inlines = (IngredientInline,)
    readonly_fields = ('count_favorite',)

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return queryset.annotate(
            _favorites_count=Count("favorites", distinct=True),
        ).select_related('author').prefetch_related('tags', 'ingredients')

    def count_favorite(self, obj):
        """Количество добавлений в Избранное"""

        return obj._favorites_count

    count_favorite.short_description = "В Избранном (раз)"


@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    """Представление избранного в админ-панели."""

    list_display = ('user', 'recipe')
    search_fields = ('user',)


@admin.register(ShoppingCart)
class ShoppingCartAdmin(admin.ModelAdmin):
    """Представление списка покупок в админ-панели."""

    list_display = ('user', 'recipe')
    search_fields = ('user',)


@admin.register(RecipeIngredient)
class RecipeIngredientAdmin(admin.ModelAdmin):
    """Представление списка покупок в админ-панели."""

    list_display = ('recipe', 'ingredient', 'amount')
    search_fields = ('recipe',)
