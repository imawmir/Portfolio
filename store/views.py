from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.utils import timezone

from .models import Product, Order, OrderItem
from core.models import Client




# Main
def main(request):
    products = Product.objects.all()
    order = Order.objects.filter(user=request.user, ordered=False).first()
    order_count = order.items.count() if order else 0
    return render(request, 'store_main.html', {'products': products, 'order_count': order_count})


# Users
def store_users(request):
    client = Client.objects.all()  # Retrieves all Client instances
    return render(request, 'store_users.html', {"client": client})


# Products
def store_products(request):
    products = Product.objects.all()
    return render(request, 'store_products.html', {'products': products})

def product_detail(request, id):
    product = Product.objects.filter(pk=id)
    order = Order.objects.filter(user=request.user, ordered=False).first()
    order_count = order.items.count() if order else 0
    return render(request, "product_detail.html", {'product': product, 'order_count': order_count})
    

# Cart
def cart(request):
    if Order.objects.filter(user=request.user,ordered=False).exists():
        order = Order.objects.get(user=request.user,ordered=False)
        order = Order.objects.filter(user=request.user, ordered=False).first()
        order_count = order.items.count() if order else 0
        return render(request,'cart.html', {'order': order, 'order_count': order_count})
    
    return render(request, 'cart.html', {'message': "Your cart is Empty"})
        

def add_to_cart(request,pk):
    # Get that Particular product if id = pk
    product = Product.objects.get(pk=pk)
    
    # Create Order Item
    order_item, created = OrderItem.objects.get_or_create(
        product = product, 
        user = request.user,
        ordered = False,
    )
    
    # Get Query set of Order Object of Particular User
    order_qs = Order.objects.filter(user=request.user,ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        if order.items.filter(product__pk = pk).exists():
            order_item.quantity += 1
            order_item.save()
            messages.info(request,"Added Quantity Item")
            return redirect("product_detail",id=pk)
        else:
            order.items.add(order_item)
            messages.info(request,"Item added to cart")
            return redirect("product_detail",id=pk)
        
    else:
        ordered_date = timezone.now()
        order = Order.objects.create(user=request.user,ordered_date=ordered_date)
        order.items.add(order_item)
        messages.info(request,"Item added to cart")
        return redirect("product_detail",id=pk)
    
def add_item(request,pk):
    # Get that Particular product if id = pk
    product = Product.objects.get(pk=pk)
    
    # Create Order Item
    order_item, created = OrderItem.objects.get_or_create(
        product = product, 
        user = request.user,
        ordered = False,
    )
    
    # Get Query set of Order Object of Particular User
    order_qs = Order.objects.filter(user=request.user,ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        if order.items.filter(product__pk = pk).exists():
            if order_item.quantity < product.inventory:
                order_item.quantity += 1
                order_item.save()
                messages.info(request,"Added Quantity Item")
                return redirect("cart")
            else:
                messages.info(request, "Sorry! Product is out of stock")
                return redirect("cart")
        else:
            order.items.add(order_item)
            messages.info(request,"Item added to cart")
            return redirect("product_detail",id=pk)
        
    else:
        ordered_date = timezone.now()
        order = Order.objects.create(user=request.user,ordered_date=ordered_date)
        order.items.add(order_item)
        messages.info(request,"Item added to cart")
        return redirect("product_detail",id=pk)


def remove_item(request,pk):
    item = get_object_or_404(Product, pk=pk)
    
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        if order.items.filter(product__pk=pk).exists():
            order_item = OrderItem.objects.filter(product=item, user=request.user, ordered=False)[0]
            if order_item.quantity > 1:
                order_item.quantity -= 1
                order_item.save()
            else:
                order_item.delete()
            messages.info(request, "Item quantity was updated")
            return redirect("cart")
        else:
            messages.info(request, "This item is not in your cart")
            return redirect("cart")
    else:
        messages.info(request, "You don't have any Order")
        return render("cart")
            