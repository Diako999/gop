from rest_framework import serializers
from .models import ProductReview, SellerReview

class ProductReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductReview
        fields = '__all__'
        read_only_fields = ['user']

class SellerReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = SellerReview
        fields = '__all__'
        read_only_fields = ['user']
