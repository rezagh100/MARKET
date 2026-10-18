from rest_framework.routers import DefaultRouter
from .views import RecommendViewSet

router = DefaultRouter()
router.register('recommendations', RecommendViewSet, basename='recommendations')

urlpatterns = router.urls