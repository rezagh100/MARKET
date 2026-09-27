from rest_framework import serializers
from .models import Offer


class OfferSerializer(serializers.ModelSerializer):
    class Meta:
        model = Offer
        fields = ['seller','product','price','stock','created_at','updated_at']
        read_only_fields = ['seller']
        
    def validate(self,attrs):
        user = self.context['request'].user
        seller = user.sellerprofile
        product = attrs['product']
        
        if Offer.objects.filter(
            seller=seller,product=product).exists():
            raise serializers.ValidationError({'product': 'You already have an offer for this product.'})
        return attrs
            
        
        