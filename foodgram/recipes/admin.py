from django.contrib import admin

from recipes.models import Favorites, Recipe, RecipeIngredients, ShoppingCart


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
    search_fields = ('name', )
    inlines = (IngredientInline, )
    prepopulated_fields = {"slug": ("name",)}

    def count_favorite(self, obj):
        """Количество добавлений в Избранное"""

        return Favorites.objects.filter(recipe=obj).count()

    count_favorite.short_description = "В Избранном (раз)"


@admin.register(Favorites)
class FavoriteAdmin(admin.ModelAdmin):
    """Представление избранного в админ-панели."""

    list_display = ('user', 'recipe')
    search_fields = ('user', )


@admin.register(ShoppingCart)
class ShoppingListAdmin(admin.ModelAdmin):
    """Представление списка покупок в админ-панели."""

    list_display = ('user', 'recipe')
    search_fields = ('user', )


@admin.register(RecipeIngredients)
class RecipeIngredientsAdmin(admin.ModelAdmin):
    """Представление списка покупок в админ-панели."""

    list_display = ('recipe', 'ingredient', 'amount')
    search_fields = ('recipe', )
