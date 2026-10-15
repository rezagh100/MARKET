from django.urls import path

from rest_framework.routers import DefaultRouter
from .views import CategoryViewSet,ProductViewSet,send_email


router =DefaultRouter()
router.register('products',ProductViewSet)
router.register('categories',CategoryViewSet)

urlpatterns = [
    path('send-email',send_email)
]

urlpatterns += router.urls