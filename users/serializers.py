from rest_framework import serializers
from .models import CustomUser
from django.contrib.auth.password_validation import validate_password
import uuid
import random
from django.core.mail import send_mail

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True)
    
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password', 'password2', 'is_seller']
    
    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Passwords must match."})
        return attrs

def create(self, validated_data):
    validated_data.pop('password2')
    password = validated_data.pop('password')

    user = CustomUser.objects.create(
        **validated_data,
        is_active=False,
        email_verification_token=str(uuid.uuid4()),  # 🎯 unique link
        phone_verification_code=str(random.randint(100000, 999999)),  # 🔢 6-digit code
    )
    user.set_password(password)
    user.save()

    # ✅ Send email (fake for now)
    if user.email:
        send_mail(
            subject="GOP Account Verification",
            message=f"Click to verify: http://localhost:8000/api/auth/verify-email/?token={user.email_verification_token}",
            from_email="no-reply@gop.com",
            recipient_list=[user.email],
            fail_silently=False
        )

    # ✅ Log the phone code (replace with SMS later)
    if user.phone_number:
        print(f"📲 Send this code to {user.phone_number}: {user.phone_verification_code}")

    return user

