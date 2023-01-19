from rest_framework import permissions


class IsAuthorOrAdmin(permissions.BasePermission):
    """Если автор или админ, можно редактировать."""

    def has_object_permission(self, request, view, obj):
        return (
            request.user.is_authenticated
            and (
                request.user == obj.author
                or request.user.is_staff
            )
        )
