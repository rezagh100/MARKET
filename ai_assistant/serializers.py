from rest_framework import serializers


class RecommendationSerializer(serializers.Serializer):
    product = serializers.CharField()
    seller = serializers.CharField()
    price = serializers.DecimalField(
        max_digits=12,
        decimal_places=2,
    )
    stock = serializers.IntegerField()