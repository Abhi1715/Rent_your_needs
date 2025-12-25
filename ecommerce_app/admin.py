from django.contrib import admin
from .models import Product
from categories_app.models import Category
# Register your models here.
admin.site.register(Product)
admin.site.register(Category)

class ProductAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}