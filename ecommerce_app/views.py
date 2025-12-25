from django.shortcuts import get_object_or_404, redirect, render
from .models import Product
from categories_app.models import Category
from .forms import SignupForm
from django.contrib.auth import login as auth_login, authenticate
from django.contrib import auth
from django.contrib.auth.forms import AuthenticationForm
# Create your views here.
def home(request):
    products = Product.objects.all()
    return render(request, 'index.html', {'products': products})



def products_by_category(request, category_name):
    category = get_object_or_404(Category, category_name=category_name)
    products = Product.objects.filter(category=category)

    return render(request, 'products_by_category.html', {
        'category': category,
        'products': products
    })

def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug)

    related_products = Product.objects.filter(
        category=product.category
    ).exclude(id=product.id)[:4]

    return render(request, 'product.html', {
        'product': product,
        'products': related_products,  
    })

def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            form.save()
            # You can add a redirect to login page or home page after successful signup
            return redirect('login')
    else:
        form = SignupForm()
    return render(request, 'signup.html', {'form': form})


def login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            user = auth.authenticate(username=username, password=password)
            if user is not None:
                auth.login(request, user)
            return redirect('home')
    form = AuthenticationForm()
    context = {
        'form': form,
    }
    return render(request, 'login.html', context)

def logout(request):
    auth.logout(request)
    return redirect('home')