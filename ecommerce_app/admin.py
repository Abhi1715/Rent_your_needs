from django.contrib import admin
from .models import Product,Order,OrderItem
from categories_app.models import Category
# Register your models here.
admin.site.register(Product)
admin.site.register(Category)
admin.site.register(Order)
admin.site.register(OrderItem)
class ProductAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}