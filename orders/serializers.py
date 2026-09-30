from rest_framework import serializers

from .models import OrderItem, Order
from offers.models import Offer


class OrderItemSerializer(serializers.ModelSerializer):

    class Meta:
        model = OrderItem
        fields = [
            'order',
            'offer',
            'quantity',
            'unit_price'
        ]
        read_only_fields = [
            'order',
            'unit_price'
        ]


class OrderSerializer(serializers.ModelSerializer):

    items = OrderItemSerializer(
        many=True,
        read_only=True
    )

    class Meta:
        model = Order
        fields = [
            'user',
            'status',
            'total_price',
            'created_at',
            'updated_at',
            'items'
        ]
        read_only_fields = [
            'user',
            'status',
            'total_price'
        ]


class OrderItemCreateSerializer(serializers.Serializer):
    offer = serializers.PrimaryKeyRelatedField(
        queryset=Offer.objects.all()
    )
    quantity = serializers.IntegerField(
        min_value=1
    )


class OrderCreateSerializer(serializers.Serializer):
    items = OrderItemCreateSerializer(
        many=True
    )