from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from .models import Product, Cart, CartItem, Order, OrderItem
from .models import Product
from categories_app.models import Category
from .forms import SignupForm
from django.contrib.auth import login as auth_login, authenticate
from django.contrib import auth
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required

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
@login_required(login_url='login')
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    cart, created = Cart.objects.get_or_create(user=request.user)

    cart_item, created = CartItem.objects.get_or_create(
        cart=cart,
        product=product
    )

    if not created:
        cart_item.quantity += 1

    cart_item.save()
    return redirect('cart_detail')

@login_required(login_url='login')
def cart_detail(request):
    cart = Cart.objects.get(user=request.user)
    return render(request, 'cart.html', {
        'cart': cart,
        'subtotal': cart.subtotal(),
        'tax': cart.tax(),
        'grand_total': cart.grand_total(),
    })

@login_required(login_url='login')
def remove_from_cart(request, item_id):
    item = get_object_or_404(CartItem, id=item_id)
    item.delete()
    return redirect('cart_detail')

@login_required(login_url='login')
def update_cart_item(request, item_id, action):
    item = get_object_or_404(CartItem, id=item_id)

    if action == 'increase':
        item.quantity += 1

    elif action == 'decrease':
        if item.quantity > 1:
            item.quantity -= 1

    item.save()
    return redirect('cart_detail')


@login_required(login_url='login')
def update_rental_days(request, item_id):
    if request.method == "POST":
        item = get_object_or_404(CartItem, id=item_id)
        days = int(request.POST.get('rental_days', 1))
        item.rental_days = max(days, 1)
        item.save()

    return redirect('cart_detail')
@login_required(login_url='login')
def checkout(request):
    cart = Cart.objects.get(user=request.user)

    if cart.items.count() == 0:
        return redirect('cart_detail')

    return render(request, 'checkout.html', {
        'cart': cart,
        'subtotal': cart.subtotal(),
        'tax': cart.tax(),
        'grand_total': cart.grand_total(),
    })


@login_required
def place_order(request):
    cart = Cart.objects.get(user=request.user)

    if cart.items.count() == 0:
        messages.error(request, "Your cart is empty.")
        return redirect("cart_detail")

    order = Order.objects.create(
        user=request.user,
        total_price=cart.grand_total()
    )

    for item in cart.items.all():
        OrderItem.objects.create(
            order=order,
            product=item.product,
            quantity=item.quantity,
            price=item.total_price()  # ✅ method call
        )

    cart.items.all().delete()

    messages.success(request, "🎉 Order placed successfully!")
    return redirect("order_history")

    
@login_required(login_url='login')
def order_history(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    return render(request, "order_history.html", {"orders": orders})

@login_required(login_url='login')
def cancel_order(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)

    if order.status in ["Shipped", "Delivered"]:
        messages.error(request, "This order cannot be cancelled.")
    else:
        order.status = "Cancelled"
        order.save()
        messages.success(request, f"Order #{order.id} cancelled successfully.")

    return redirect("order_history")
    

