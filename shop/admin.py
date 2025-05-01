from django.contrib import admin
from .models import Product, ProductCategory, Shop

admin.site.register(Product)

class ProductCategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')  # Show both ID and name
admin.site.register(ProductCategory, ProductCategoryAdmin)
admin.site.register(Shop)

# Register your models here.
