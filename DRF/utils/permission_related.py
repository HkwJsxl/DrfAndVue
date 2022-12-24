from rest_framework.permissions import BasePermission


class RolePermission(BasePermission):
    def has_permission(self, request, view):
        if request.user.role == 2:
            return True
        return False

    def has_object_permission(self, request, view, obj):
        return True
