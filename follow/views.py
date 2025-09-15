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
        serializer.save(follower=self.request.user)

    @action(detail=True, methods=['delete'], url_path='unfollow')
    def unfollow(self, request, pk=None):
        follow = self.get_object()
        if follow.follower != request.user:
            return Response({"detail": "Unauthorized"}, status=403)
        follow.delete()
        return Response({"detail": "Unfollowed successfully."})
