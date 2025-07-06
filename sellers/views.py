from rest_framework import generics, permissions
from .models import SellerProfile
from .serializers import SellerProfileSerializer

class SellerProfileDetailView(generics.RetrieveUpdateAPIView):
    serializer_class = SellerProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return SellerProfile.objects.get(user=self.request.user)
