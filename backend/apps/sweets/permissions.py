from rest_framework.permissions import BasePermission


class IsAdminUserRole(BasePermission):
    """
    Allows access only to admin users.
    """

    def has_permission(self, request, view):
        return request.user and request.user.is_staff
