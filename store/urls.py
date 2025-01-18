from django.urls import path
from . import views

urlpatterns = [
    path('', views.main, name='store_main'),
    path('store_users/', views.store_users, name='store_users'),
    path('store_products/', views.store_products, name='store_products'),
    path('product_detail/<int:id>', views.product_detail, name='product_detail'),
    path('cart/', views.cart, name='cart'),
    path('add_to_cart/<pk>', views.add_to_cart, name='add_to_cart'),
    path('add_item/<pk>', views.add_item, name='add_item'),
    path('remove_item/<pk>', views.remove_item, name='remove_item'),
]