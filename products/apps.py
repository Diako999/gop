from django.apps import AppConfig


class ProductsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'products'
    
    def ready(self):
        # Create default category if it doesn't exist
        from .models import Category
        Category.objects.get_or_create(name='Fabric', defaults={'name': 'Fabric'})