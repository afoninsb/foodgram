from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

from users.models import Subscription


class MyUserAdmin(UserAdmin):
    list_filter = UserAdmin.list_filter + ('username', 'email')


admin.site.unregister(User)
admin.site.register(User, MyUserAdmin)


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    """Представление подписок в админ-панели."""

    list_display = (
        'subscriber',
        'author',
    )
