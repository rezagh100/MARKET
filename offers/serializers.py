from rest_framework import serializers
from .models import Offer


class OfferSerializer(serializers.ModelSerializer):
    class Meta:
        model = Offer
        fields = [
            'seller',
            'product',
            'price',
            'stock',
            'created_at',
            'updated_at'
        ]
        read_only_fields = ['seller']

    def validate(self, attrs):
        user = self.context['request'].user
        seller = user.sellerprofile

        product = attrs.get(
            'product',
            self.instance.product if self.instance else None
        )

        queryset = Offer.objects.filter(
            seller=seller,
            product=product
        )

        if self.instance:
            queryset = queryset.exclude(
                pk=self.instance.pk
            )

        if queryset.exists():
            raise serializers.ValidationError({
                'product': 'You already have an offer for this product.'
            })

        return attrs