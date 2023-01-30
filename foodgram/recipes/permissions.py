from rest_framework import permissions


class IsAuthor(permissions.BasePermission):
    """Если автор, можно редактировать и удалять."""

    def has_object_permission(self, request, view, obj):
        return request.user.is_authenticated and request.user == obj.author
