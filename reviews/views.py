from rest_framework import viewsets, permissions
from .models import ProductReview, SellerReview
from .serializers import ProductReviewSerializer, SellerReviewSerializer
from orders.models import Order
from products.models import Product

class IsVerifiedBuyer(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_active

    def has_object_permission(self, request, view, obj):
        return obj.user == request.user

class ProductReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ProductReviewSerializer
    permission_classes = [IsVerifiedBuyer]

    def get_queryset(self):
        return ProductReview.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        product_id = self.request.data.get('product')
        if not Order.objects.filter(product_id=product_id, buyer=self.request.user, status='paid').exists():
            raise serializers.ValidationError("You can only review products you’ve purchased.")
        serializer.save(user=self.request.user)

class SellerReviewViewSet(viewsets.ModelViewSet):
    serializer_class = SellerReviewSerializer
    permission_classes = [IsVerifiedBuyer]

    def get_queryset(self):
        return SellerReview.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        seller_id = self.request.data.get('seller')
        if not Order.objects.filter(product__seller__user_id=seller_id, buyer=self.request.user, status='paid').exists():
            raise serializers.ValidationError("You can only review sellers you’ve bought from.")
        serializer.save(user=self.request.user)
