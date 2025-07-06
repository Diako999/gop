from django.db import models
from django.conf import settings

class SellerProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='seller_profile')
    store_name = models.CharField(max_length=150)
    bio = models.TextField(blank=True)
    banner_image = models.ImageField(upload_to='sellers/banners/', blank=True, null=True)
    id_document = models.FileField(upload_to='sellers/ids/', blank=True, null=True)
    artisan_certificate = models.FileField(upload_to='sellers/certificates/', blank=True, null=True)
    is_approved = models.BooleanField(default=False)
    join_date = models.DateField(auto_now_add=True)
    average_rating = models.FloatField(default=0)
    followers_count = models.IntegerField(default=0)

    def __str__(self):
        return self.store_name
