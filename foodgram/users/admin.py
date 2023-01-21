from django.contrib import admin

from users.models import Subscription


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    """Представление подписок в админ-панели."""

    list_display = (
        'subscriber',
        'author',
    )
    search_fields = ('subscriber', 'author')
