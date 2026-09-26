from rest_framework.viewsets import ModelViewSet
from products.models import Category, Product
from .serializers import ProductSerializer,CategorySerializer
from .permissions import IsOwnerOrCustomer

class ProductViewSet(ModelViewSet):
    permission_classes = [IsOwnerOrCustomer]
    serializer_class = ProductSerializer
    queryset = Product.objects.all()
    
    
class CategoryViewSet(ModelViewSet):
    permission_classes = [IsOwnerOrCustomer]
    serializer_class = CategorySerializer
    queryset = Category.objects.all()