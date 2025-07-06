from rest_framework import viewsets, permissions
from .models import Product
from .serializers import ProductSerializer
from sellers.models import SellerProfile

class IsSellerVerified(permissions.BasePermission):
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated and 
            request.user.is_seller and 
            request.user.is_verified
        )

    def has_object_permission(self, request, view, obj):
        return obj.seller.user == request.user

class ProductViewSet(viewsets.ModelViewSet):
    serializer_class = ProductSerializer
    permission_classes = [IsSellerVerified]

    def get_queryset(self):
        return Product.objects.filter(seller__user=self.request.user)

    def perform_create(self, serializer):
        seller_profile = SellerProfile.objects.get(user=self.request.user)
        serializer.save(seller=seller_profile)
