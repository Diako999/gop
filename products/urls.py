from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ProductViewSet
from .views import FollowedSellersFeedView

router = DefaultRouter()
router.register(r'my-products', ProductViewSet, basename='my-products')

urlpatterns = router.urls

urlpatterns += [
    path('followed-sellers/feed/', FollowedSellersFeedView.as_view(), name='followed-sellers-feed'),
]