from django.contrib import admin

from recipes.models import Ingredient, Tag


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    """Представление тэгов в админ-панели."""

    list_display = (
        'name',
        'slug',
        'color',
    )
    search_fields = ('name',)


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    """Представление ингредиентов в админ-панели."""

    list_display = (
        'name',
        'unit',
    )
    search_fields = ('name',)
