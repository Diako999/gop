from rest_framework.routers import DefaultRouter
from .views import ProductReviewViewSet, SellerReviewViewSet

router = DefaultRouter()
router.register(r'product-reviews', ProductReviewViewSet)
router.register(r'seller-reviews', SellerReviewViewSet)

urlpatterns = router.urls
