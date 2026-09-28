from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated

from .models import Offer
from .permissions import IsSeller,IsOfferOwner
from .serializers import OfferSerializer


class OfferViewSet(ModelViewSet):
    permission_classes = [IsSeller,IsOfferOwner]
    queryset = Offer.objects.all()
    serializer_class = OfferSerializer
    
    def perform_create(self, serializer):
        serializer.save(seller=self.request.user.sellerprofile)