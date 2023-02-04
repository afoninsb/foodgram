from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from users.models import Subscription, User


@admin.register(User)
class UserAdmin(UserAdmin):
    list_filter = UserAdmin.list_filter + ('username', 'email')


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    """Представление подписок в админ-панели."""

    list_display = (
        'subscriber',
        'author',
    )
