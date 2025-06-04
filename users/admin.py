from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ('username', 'email', 'is_seller', 'is_verified', 'is_staff')
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('is_seller', 'is_verified', 'profile_image')}),
    )

admin.site.register(CustomUser, CustomUserAdmin)
