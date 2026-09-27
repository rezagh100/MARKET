from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsSeller(BasePermission):
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        
        return hasattr(request.user, 'sellerprofile')