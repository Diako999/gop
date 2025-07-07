from django.urls import path
from .views import SellerProfileDetailView, SellerDashboardView, SellerMonthlyStatsView, SellerOfTheMonthView, ProductOfTheMonthView, TopSellersView

urlpatterns = [
    path('me/', SellerProfileDetailView.as_view(), name='seller-profile'),
    path('dashboard/', SellerDashboardView.as_view(), name='seller-dashboard'),
    path('dashboard/monthly/', SellerMonthlyStatsView.as_view(), name='seller-monthly-stats'),
    path('dashboard/seller-of-the-month/', SellerOfTheMonthView.as_view(), name='seller-of-the-month'),
    path('dashboard/product-of-the-month/', ProductOfTheMonthView.as_view(), name='product-of-the-month'),
    path('dashboard/top-sellers/', TopSellersView.as_view(), name='top-sellers'),


]
