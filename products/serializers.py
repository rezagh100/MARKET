from rest_framework.serializers import ModelSerializer
from products.models import Category, Product


class ProductSerializer(ModelSerializer):
    class Meta:
        model = Product
        fields = ['title','description','category']


class CategorySerializer(ModelSerializer):
    class Meta:
        model = Category
        fields = ['name','description']
