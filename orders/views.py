from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

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

    def get_queryset(self):
        return Order.objects.filter(
            user=self.request.user
        )

    def create(self, request, *args, **kwargs):
        serializer = OrderCreateSerializer(
            data=request.data
        )

        serializer.is_valid(
            raise_exception=True
        )

        try:
            order = OrderService().create_order(
                user=request.user,
                items=serializer.validated_data['items']
            )

        except InsufficientStockError as exc:
            return Response(
                {'detail': str(exc)},
                status=status.HTTP_400_BAD_REQUEST
            )

        return Response(
            OrderSerializer(order).data,
            status=status.HTTP_201_CREATED
        )

    @action(
        detail=True,
        methods=['post']
    )
    def cancel(self, request, pk=None):
        order = self.get_object()

        cancelled = OrderService().cancel_order(
            user=request.user,
            order=order
        )

        if not cancelled:
            return Response(
                {'detail': 'Order cannot be cancelled.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        return Response(
            {'detail': 'Order cancelled successfully.'},
            status=status.HTTP_200_OK
        )