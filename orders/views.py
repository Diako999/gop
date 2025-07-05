import requests
from django.conf import settings
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from .models import Order
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from rest_framework import viewsets, permissions
from .models import Order
from .serializers import OrderSerializer
from products.models import Product

class OrderViewSet(viewsets.ModelViewSet):
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_seller:
            # Show orders for seller's products
            return Order.objects.filter(product__seller__user=user)
        return Order.objects.filter(buyer=user)

    def perform_create(self, serializer):
        product = Product.objects.get(id=self.request.data['product'])
        quantity = int(self.request.data['quantity'])
        total_price = product.price * quantity

        serializer.save(
            buyer=self.request.user,
            total_price=total_price
        )
        
    @action(detail=True, methods=['post'], url_path='pay')
    def pay_order(self, request, pk=None):
        order = self.get_object()
        if order.status != 'pending':
            return Response({"detail": "This order is already processed."}, status=400)

        merchant_id = settings.ZARINPAL_MERCHANT_ID
        callback_url = f"http://localhost:8000/api/payment/verify/?order_id={order.id}"

        data = {
            "MerchantID": merchant_id,
            "Amount": int(order.total_price),
            "Description": f"Payment for order #{order.id}",
            "CallbackURL": callback_url,
        }

        headers = {'content-type': 'application/json'}
        res = requests.post("https://api.zarinpal.com/pg/v4/payment/request.json", json=data, headers=headers)

        response_data = res.json().get("data", {})
        if res.status_code == 200 and response_data.get("Authority"):
            authority = response_data["Authority"]
            payment_url = f"https://www.zarinpal.com/pg/StartPay/{authority}"
            return Response({"payment_url": payment_url}, status=200)
        else:
            return Response({"error": "Zarinpal request failed."}, status=500)    
class VerifyPaymentView(APIView):
    def get(self, request):
        order_id = request.GET.get("order_id")
        authority = request.GET.get("Authority")
        status_str = request.GET.get("Status")

        order = get_object_or_404(Order, id=order_id)

        if status_str != "OK":
            return Response({"detail": "Payment cancelled or failed."}, status=400)

        merchant_id = settings.ZARINPAL_MERCHANT_ID
        verify_data = {
            "MerchantID": merchant_id,
            "Amount": int(order.total_price),
            "Authority": authority
        }

        res = requests.post("https://api.zarinpal.com/pg/v4/payment/verify.json", json=verify_data)
        result = res.json().get("data", {})

        if result.get("Code") == 100:
            order.status = "paid"
            order.save()
            return Response({"detail": "Payment successful!"}, status=200)
        else:
            return Response({"detail": "Payment verification failed."}, status=400)