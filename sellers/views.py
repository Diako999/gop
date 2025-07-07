from rest_framework import generics, permissions
from .models import SellerProfile
from .serializers import SellerProfileSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from products.models import Product
from orders.models import Order
from reviews.models import SellerReview
from django.db.models import Sum, Count, Avg
from django.utils.timezone import now
from django.db.models.functions import TruncMonth
from django.db.models import Count

class SellerProfileDetailView(generics.RetrieveUpdateAPIView):
    serializer_class = SellerProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return SellerProfile.objects.get(user=self.request.user)

class SellerDashboardView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        if not user.is_seller or not user.is_verified:
            return Response({"detail": "Access denied"}, status=403)

        # Products
        products = Product.objects.filter(seller__user=user)
        total_products = products.count()

        # Orders
        orders = Order.objects.filter(product__seller__user=user, status='paid')
        total_orders = orders.count()
        total_sales = orders.aggregate(Sum('total_price'))['total_price__sum'] or 0

        # Reviews
        avg_rating = SellerReview.objects.filter(seller=user).aggregate(Avg('rating'))['rating__avg'] or 0

        # Top product by number of orders
        top_product_data = (
            orders.values('product__name')
            .annotate(order_count=Count('id'))
            .order_by('-order_count')
            .first()
        )
        top_product = top_product_data['product__name'] if top_product_data else None

        return Response({
            "total_products": total_products,
            "total_orders": total_orders,
            "total_sales": total_sales,
            "average_rating": round(avg_rating, 1),
            "top_product": top_product,
        })
    
class SellerMonthlyStatsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        if not user.is_seller or not user.is_verified:
            return Response({"detail": "Access denied"}, status=403)

        orders = Order.objects.filter(
            product__seller__user=user,
            status='paid',
            created_at__year=now().year
        )

        data = (
            orders.annotate(month=TruncMonth('created_at'))
            .values('month')
            .annotate(
                total_sales=Sum('total_price'),
                order_count=Count('id')
            )
            .order_by('month')
        )

        return Response(data)
    
class SellerOfTheMonthView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        current_month = now().month
        current_year = now().year

        top_seller_data = (
            Order.objects.filter(status='paid', created_at__year=current_year, created_at__month=current_month)
            .values('product__seller__user')
            .annotate(total_orders=Count('id'))
            .order_by('-total_orders')
            .first()
        )

        if not top_seller_data:
            return Response({"detail": "No sellers found for this month"}, status=404)

        seller_id = top_seller_data['product__seller__user']
        seller = CustomUser.objects.get(id=seller_id)

        return Response({
            "seller_id": seller.id,
            "seller_name": seller.username,
            "profile_image": seller.profile_image.url if seller.profile_image else None,
            "total_orders": top_seller_data['total_orders'],
        })
    
class ProductOfTheMonthView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        current_month = now().month
        current_year = now().year

        product_data = (
            Order.objects.filter(status='paid', created_at__year=current_year, created_at__month=current_month)
            .values('product')
            .annotate(order_count=Count('id'))
            .order_by('-order_count')
            .first()
        )

        if not product_data:
            return Response({"detail": "No product data for this month"}, status=404)

        product_id = product_data['product']
        product = Product.objects.get(id=product_id)

        return Response({
            "product_id": product.id,
            "product_name": product.name,
            "image": product.image.url if hasattr(product, 'image') else None,
            "order_count": product_data['order_count'],
            "seller": product.seller.user.username,
        })
    
class TopSellersView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        current_month = now().month
        current_year = now().year

        seller_stats = (
            Order.objects.filter(status='paid', created_at__year=current_year, created_at__month=current_month)
            .values('product__seller__user')
            .annotate(total_orders=Count('id'))
            .order_by('-total_orders')[:5]
        )

        response = []
        for entry in seller_stats:
            user_id = entry['product__seller__user']
            user = CustomUser.objects.get(id=user_id)
            response.append({
                "seller_id": user.id,
                "seller_name": user.username,
                "profile_image": user.profile_image.url if user.profile_image else None,
                "total_orders": entry['total_orders'],
            })

        return Response(response)
