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
]