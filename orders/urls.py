from rest_framework.routers import DefaultRouter
from .views import OrderViewSet


router = DefaultRouter()

router.register('order',OrderViewSet)

urlpatterns = router.urls
