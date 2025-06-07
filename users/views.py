from django.shortcuts import render
# Create your views here.
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from .serializers import RegisterSerializer
from .models import CustomUser
from rest_framework import permissions


class RegisterView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = RegisterSerializer


class VerifyEmailView(APIView):
    def get(self, request):
        token = request.GET.get('token')
        try:
            user = CustomUser.objects.get(email_verification_token=token)
            user.is_active = True
            user.email_verification_token = None
            user.save()
            return Response({"detail": "Email verified successfully."}, status=200)
        except CustomUser.DoesNotExist:
            return Response({"detail": "Invalid or expired token."}, status=400)
        
class VerifyPhoneView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        phone = request.data.get("phone_number")
        code = request.data.get("code")

        try:
            user = CustomUser.objects.get(phone_number=phone, phone_verification_code=code)
            user.is_active = True
            user.phone_verification_code = None
            user.save()
            return Response({"detail": "Phone number verified."}, status=200)
        except CustomUser.DoesNotExist:
            return Response({"detail": "Invalid code or phone number."}, status=400)