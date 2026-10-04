from rest_framework.routers import DefaultRouter
from .views import PaymentViewSet
router = DefaultRouter()

router.register('pay',PaymentViewSet)

urlpatterns = router.urls