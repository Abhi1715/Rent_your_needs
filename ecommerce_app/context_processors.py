from unicodedata import category

from django.shortcuts import get_object_or_404
from .models import Category, Product


def get_categories(request):
    categories = Category.objects.all()
    return dict(categories=categories)


def get_all_products(request):
    products = Product.objects.all()
    return dict(all_products=products)