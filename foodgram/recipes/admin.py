from django.contrib import admin

from recipes.models import Favorites, Recipe, ShoppingList


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    """Представление рецептов в админ-панели."""

    list_display = (
        'author',
        'name',
        'text',
        'cooking_time',
        'image',
        'pub_date'
    )
    search_fields = ('name',)


@admin.register(Favorites)
class FavoriteAdmin(admin.ModelAdmin):
    """Представление избранного в админ-панели."""

    list_display = (
        'user',
        'recipe',
    )
    search_fields = ('user',)


@admin.register(ShoppingList)
class ShoppingListAdmin(admin.ModelAdmin):
    """Представление списка покупок в админ-панели."""

    list_display = (
        'user',
        'recipe',
    )
    search_fields = ('user',)
