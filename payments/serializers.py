from rest_framework import serializers
from .models import Payment

class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = ['order','amount','status','created_at']
        read_only_fields = ['order','amount','status','created_at']