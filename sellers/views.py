from rest_framework.viewsets import ModelViewSet
from .serializers import SellerProfileSerializer
from sellers.models import SellerProfile
from rest_framework.permissions import IsAuthenticated

class SellerProfileViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = SellerProfile.objects.all()
    serializer_class = SellerProfileSerializer
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
    