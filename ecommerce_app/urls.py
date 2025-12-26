from django.urls import path
from . import views

urlpatterns = [
    
    path('',views.home, name='home'),
   # path('<int:category_id>/', views.posts_by_category, name='posts_by_category'),
   path('product/<slug:slug>/', views.product_detail, name='product_detail'),
   path('category/<str:category_name>/', views.products_by_category, name='products_by_category'),
   path('signup/', views.signup, name='signup'),
   path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('add-to-cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/', views.cart_detail, name='cart_detail'),
    path('remove/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('cart/update/<int:item_id>/<str:action>/',
         views.update_cart_item,
         name='update_cart_item'),

    path('cart/update-days/<int:item_id>/',
         views.update_rental_days,
         name='update_rental_days'),
    path('checkout/', views.checkout, name='checkout'),
    path("place-order/", views.place_order, name="place_order"),
    path("orders/", views.order_history, name="order_history"),
    path("cancel-order/<int:order_id>/", views.cancel_order, name="cancel_order"),



]