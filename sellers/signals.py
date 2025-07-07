from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import CustomUser
from sellers.models import Seller

@receiver(post_save, sender=CustomUser)
def create_seller_profile(sender, instance, created, **kwargs):
    if created and instance.is_seller:
        Seller.objects.create(user=instance, store_name=instance.username)
