from django.contrib import admin

from tags.models import Tag


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    """Представление тэгов в админ-панели."""

    list_display = (
        'name',
        'slug',
        'color',
    )
    search_fields = ('name',)
