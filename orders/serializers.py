from rest_framework import serializers

from .models import OrderItem, Order


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
