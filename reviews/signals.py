from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import ProductReview, SellerReview
from products.models import Product
from users.models import CustomUser
from django.db.models import Avg

@receiver([post_save, post_delete], sender=ProductReview)
def update_product_rating(sender, instance, **kwargs):
    product = instance.product
    avg = product.reviews.aggregate(Avg('rating'))['rating__avg'] or 0
    product.average_rating = round(avg, 1)
    product.save()

@receiver([post_save, post_delete], sender=SellerReview)
def update_seller_rating(sender, instance, **kwargs):
    seller = instance.seller
    avg = seller.seller_reviews.aggregate(Avg('rating'))['rating__avg'] or 0
    seller.average_rating = round(avg, 1)
    seller.save()
