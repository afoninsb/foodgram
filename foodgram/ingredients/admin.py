from django.contrib import admin

from ingredients.models import Ingredient


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    """Представление ингредиентов в админ-панели."""

    list_display = (
        'name',
        'measurement_unit',
    )
    search_fields = ('name', )
