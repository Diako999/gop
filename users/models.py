from django.contrib.auth.models import AbstractUser
from django.db import models

def profile_image_upload_path(instance, filename):
    return f"profiles/user_{instance.id}/{filename}"

from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    is_seller = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)
    profile_image = models.ImageField(upload_to='profiles/', blank=True, null=True)

    # ✅ Verification fields
    email_verification_token = models.CharField(max_length=100, blank=True, null=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    phone_verification_code = models.CharField(max_length=6, blank=True, null=True)

    is_active = models.BooleanField(default=False)  # Only true after verifying

    def __str__(self):
        return self.username

