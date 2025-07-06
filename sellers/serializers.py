from rest_framework import serializers
from .models import SellerProfile

class SellerProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = SellerProfile
        fields = [
            'store_name',
            'bio',
            'banner_image',
            'id_document',
            'artisan_certificate',
            'is_approved',
            'join_date',
            'average_rating',
            'followers_count',
        ]
        read_only_fields = ['is_approved', 'created_at']
