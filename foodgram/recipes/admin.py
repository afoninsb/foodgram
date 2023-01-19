from django.contrib import admin

from recipes.models import Recipe


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
