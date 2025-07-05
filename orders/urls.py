from rest_framework.routers import DefaultRouter
from .views import OrderViewSet
from .views import VerifyPaymentView
from django.urls import path

router = DefaultRouter()
router.register(r'orders', OrderViewSet, basename='orders')

urlpatterns = router.urls

urlpatterns += [
    path('payment/verify/', VerifyPaymentView.as_view(), name='verify-payment'),
]
