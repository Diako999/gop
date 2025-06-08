from rest_framework.views import APIView
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from .serializers import RegisterSerializer
from .models import CustomUser
from rest_framework import permissions
from rest_framework_simplejwt.tokens import RefreshToken
import kavenegar


class RegisterView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = RegisterSerializer


class VerifyEmailView(APIView):
    def get(self, request):
        token = request.GET.get('token')
        try:
            user = CustomUser.objects.get(email_verification_token=token)
            user.is_active = True
            user.email_verification_token = None  # Clear verification token
            user.save()

            # Create JWT token for the user
            refresh = RefreshToken.for_user(user)
            access_token = str(refresh.access_token)

            # Return the access token to the user
            return Response({
                'detail': 'Email verified successfully.',
                'access_token': access_token,
            }, status=200)
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
            user.phone_verification_code = None  # Clear verification code
            user.save()

            # Send success response
            return Response({"detail": "Phone number verified."}, status=200)
        except CustomUser.DoesNotExist:
            return Response({"detail": "Invalid code or phone number."}, status=400)

    def send_sms(self, phone_number, code):
        # Kavenegar API key (you should securely store this in your settings file)
        api_key = 'YOUR_KAVENEGAR_API_KEY'
        
        # Create the Kavenegar API instance
        kavenegar_api = kavenegar.KavenegarAPI(api_key)

        # Send SMS
        params = {
            'receptor': phone_number,  # User's phone number
            'message': f"Your verification code is: {code}",
        }
        
        try:
            response = kavenegar_api.send('YourSenderName', params)
            return response
        except Exception as e:
            return str(e)