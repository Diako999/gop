from rest_framework.routers import DefaultRouter
from .views import ProductViewSet

router = DefaultRouter()
router.register(r'my-products', ProductViewSet, basename='my-products')

urlpatterns = router.urls
