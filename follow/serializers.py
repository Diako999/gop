from .models import Follow
from rest_framework import serializers

class FollowSerializer(serializers.ModelSerializer):
    follower_username = serializers.CharField(source='follower.username', read_only=True)
    seller_username = serializers.CharField(source='seller.username', read_only=True)

    class Meta:
        model = Follow
        fields = [
            'id',
            'follower', 'follower_username',
            'seller', 'seller_username',
            'created_at'
        ]
        read_only_fields = ['follower', 'created_at']
