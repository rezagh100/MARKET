from rest_framework.viewsets import ModelViewSet
from .models import Payment
from .serializers import PaymentSerializer
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from .services import PaymentService
from rest_framework.response import Response
from rest_framework import status

class PaymentViewSet(ModelViewSet):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return Payment.objects.filter(order__user=self.request.user)
    
    @action(detail=True,methods=['post'])
    def pay(self,request,pk=None):
        payment = self.get_object()
        result = PaymentService().pay(payment=payment)
        if result:
            return Response({'detail':'Payment operation was successful'},status=status.HTTP_200_OK)
        return Response({'detail':'Payment cannot be paid.'},status=status.HTTP_400_BAD_REQUEST)