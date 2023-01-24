from django.contrib import admin

from tags.models import Tag
from recipes.models import Favorites, Recipe, RecipeIngredients, RecipeTags, ShoppingList


class Tags(admin.SimpleListFilter):
    """Фильтр по тэгам."""

    title = ('Тэги')
    parameter_name = 'tag'

    def lookups(self, request, model_admin):
        """Список тэгов."""

        tags = Tag.objects.all()
        return [(tag.slug, tag.name) for tag in tags]

    def queryset(self, request, queryset):
        """Фильтр к queryset."""

        if not self.value():
            return queryset
        tags = RecipeTags.objects.\
            filter(tag__slug=self.value()).values('recipe_id')
        return queryset.filter(id__in=tags)


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    """Представление рецептов в админ-панели."""

    def count_favorite(self, obj):
        """Количество добавлений в Избранное"""

        return Favorites.objects.filter(recipe=obj).count()

    count_favorite.short_description = "В Избранном (раз)"

    list_display = (
        'name',
        'author',
        'text',
        'cooking_time',
        'image',
        'count_favorite'
    )
    list_filter = (Tags, )
    search_fields = ('name', )


@admin.register(Favorites)
class FavoriteAdmin(admin.ModelAdmin):
    """Представление избранного в админ-панели."""

    list_display = (
        'user',
        'recipe',
    )
    search_fields = ('user', )


@admin.register(ShoppingList)
class ShoppingListAdmin(admin.ModelAdmin):
    """Представление списка покупок в админ-панели."""

    list_display = (
        'user',
        'recipe',
    )
    search_fields = ('user', )


@admin.register(RecipeIngredients)
class RecipeIngredientsAdmin(admin.ModelAdmin):
    """Представление списка покупок в админ-панели."""

    list_display = (
        'recipe',
        'ingredient',
        'amount',
    )
    search_fields = ('recipe', )


@admin.register(RecipeTags)
class RecipeTagsAdmin(admin.ModelAdmin):
    """Представление списка покупок в админ-панели."""

    list_display = (
        'recipe',
        'tag',
    )
    search_fields = ('recipe', )
