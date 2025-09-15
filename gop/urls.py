from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/auth/', include('users.urls')),  # register now at /api/auth/register/
    # ✅ JWT login
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/', include('orders.urls')),
    path('api/reviews/', include('reviews.urls')),
    path('api/products/', include('products.urls')),
    path('api/seller/', include('sellers.urls')),
    path('api/notifications/', include('notifications.urls')),
    path('api/follow/', include('follow.urls')),



]
