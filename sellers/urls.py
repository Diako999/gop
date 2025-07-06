from django.urls import path
from .views import SellerProfileDetailView

urlpatterns = [
    path('me/', SellerProfileDetailView.as_view(), name='seller-profile'),
]
