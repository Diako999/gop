from .models import Follow
from .serializers import FollowSerializer
from rest_framework import viewsets, permissions
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError


class FollowViewSet(viewsets.ModelViewSet):
    serializer_class = FollowSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Follow.objects.filter(follower=self.request.user)

    def perform_create(self, serializer):
        seller = serializer.validated_data['seller']

        if not seller.is_seller:
            raise ValidationError("Target user is not a seller.")

        # Check if the follow already exists
        existing_follow = Follow.objects.filter(follower=self.request.user, seller=seller).first()
        if existing_follow:
            raise ValidationError("You are already following this seller.")

        serializer.save(follower=self.request.user)


    @action(detail=True, methods=['delete'], url_path='unfollow')
    def unfollow(self, request, pk=None):
        follow = self.get_object()
        if follow.follower != request.user:
            return Response({"detail": "Unauthorized"}, status=403)
        follow.delete()
        return Response({"detail": "Unfollowed successfully."})
    
    @action(detail=False, methods=['get'], url_path='followers')
    def followers(self, request):
        queryset = Follow.objects.filter(seller=request.user)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)