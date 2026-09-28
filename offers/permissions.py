from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsSeller(BasePermission):
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        
        return hasattr(request.user, 'sellerprofile')
    
      
class IsOfferOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True

        return request.user.sellerprofile == obj.seller
            