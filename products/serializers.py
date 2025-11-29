from rest_framework import serializers
from .models import Product

class ProductSerializer(serializers.ModelSerializer):
    seller_id = serializers.SerializerMethodField()
    
    class Meta:
        model = Product
        fields = ['id', 'category', 'name', 'description', 'price',
            'stock', 'is_active', 'created_at', 'average_rating', 'seller_id']
        read_only_fields = ['id', 'created_at', 'average_rating', 'seller_id']
    
    def get_seller_id(self, obj):
        return obj.seller.user.id if obj.seller and obj.seller.user else None
