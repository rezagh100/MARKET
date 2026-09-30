from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated

from orders.models import Order
from orders.services import OrderService, InsufficientStockError

from .serializers import (
    OrderCreateSerializer,
    OrderSerializer,
)


class OrderViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    def create(self, request, *args, **kwargs):
        serializer = OrderCreateSerializer(data=request.data)

        serializer.is_valid(raise_exception=True)

        try:
            order = OrderService().create_order(
                user=request.user,
                items=serializer.validated_data['items']
            )

        except InsufficientStockError as ise:
            return Response(
                {'detail': str(ise)},
                status=status.HTTP_400_BAD_REQUEST
            )

        return Response(
            OrderSerializer(order).data,
            status=status.HTTP_201_CREATED
        )