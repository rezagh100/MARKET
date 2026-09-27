from rest_framework.routers import DefaultRouter
from .views import SellerProfileViewSet

router = DefaultRouter()

router.register('seller-profiles',SellerProfileViewSet)

urlpatterns = router.urls