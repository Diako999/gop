from django.contrib.auth.models import AbstractUser
from django.db import models

def profile_image_upload_path(instance, filename):
    return f"profiles/user_{instance.id}/{filename}"

class CustomUser(AbstractUser):
    is_seller = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)  # For approved sellers
    profile_image = models.ImageField(
        upload_to=profile_image_upload_path,
        blank=True,
        null=True
    )

    def __str__(self):
        return self.username
