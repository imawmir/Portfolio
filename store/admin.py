from django.contrib import admin
from . models import Category, Product, OrderItem, Order, Address



# REGISTERS
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'title']
    

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'category', 'price', 'inventory']
    

@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'final_price']
    

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'ordered_date', 'total_price']


@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = ['id', 'user']