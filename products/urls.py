from rest_framework.routers import DefaultRouter
from .views import CategoryViewSet,ProductViewSet


router =DefaultRouter()
router.register('products',ProductViewSet)
router.register('categories',CategoryViewSet)

urlpatterns = router.urls