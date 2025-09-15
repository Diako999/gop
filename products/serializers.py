from rest_framework import serializers
from .models import Product

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'category', 'name', 'description', 'price',
            'stock', 'is_active', 'created_at', 'average_rating']
        read_only_fields = ['id', 'created_at', 'average_rating']
