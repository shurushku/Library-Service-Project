from rest_framework.permissions import SAFE_METHODS, BasePermission


class IfAuthenticatedReadOnly(BasePermission):
    def has_permission(self, request, view):
        return bool(
            request.method in SAFE_METHODS
            and request.user
            and request.user.is_authenticated
        )
