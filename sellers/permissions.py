from rest_framework.permissions import BasePermission


class IsStoreOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.user == request.user