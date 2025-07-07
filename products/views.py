from rest_framework import viewsets, permissions, generics
from .models import Product
from .serializers import ProductSerializer
from sellers.models import SellerProfile
from notifications.tasks import send_notification
from follow.models import Follow

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
        # Notify followers
        followers = Follow.objects.filter(seller=self.request.user)
        for follow in followers:
            send_notification.delay(
                follow.follower.id,
                f"{self.request.user.username} just added a new product: {Product.name}"
            )

class FollowedSellersFeedView(generics.ListAPIView):
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        followed_seller_ids = Follow.objects.filter(follower=self.request.user).values_list('seller_id', flat=True)
        return Product.objects.filter(seller__user_id__in=followed_seller_ids, is_active=True).order_by('-created_at')
