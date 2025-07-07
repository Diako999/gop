from .models import Follow
from rest_framework import serializers

class FollowSerializer(serializers.ModelSerializer):
    class Meta:
        model = Follow
        fields = ['id', 'follower', 'seller', 'created_at']
        read_only_fields = ['follower', 'created_at']
