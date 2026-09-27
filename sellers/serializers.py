from rest_framework import serializers
from .models import SellerProfile


class SellerProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = SellerProfile
        fields = ['id', 'user', 'store_name', 'description']
        read_only_fields = ['user']

    def validate(self, attrs):
        user = self.context['request'].user

        if SellerProfile.objects.filter(user=user).exists():
            raise serializers.ValidationError(
                "Each user can have only one seller profile."
            )

        return attrs