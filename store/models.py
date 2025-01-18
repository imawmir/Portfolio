from django.db import models
from django.urls import reverse
from django.core.validators import MinValueValidator
from django.contrib.auth.models import User


# Category
class Category(models.Model):
    title = models.CharField(max_length=255)
    
    def __str__(self):
        return self.title

# Product
class Product(models.Model):
    title = models.CharField(max_length=255)
    category = models.ForeignKey('Category', on_delete=models.CASCADE)
    description = models.TextField()
    price = models.FloatField(default=1.0, validators=[MinValueValidator(0.01)])
    inventory = models.IntegerField(default=0, validators=[MinValueValidator(0)])
    image = models.ImageField(upload_to='store')
    
    def __str__(self):
        return self.title
    
    def get_add_to_cart_url(self):
        return reverse("core:add-to-cart", kwargs={"pk": self.pk})
    
    
# OrderItem
class OrderItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    ordered = models.BooleanField(default=False)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1, validators=[MinValueValidator(1)])
    
    def __str__(self):
        return f"{self.quantity} of {self.product}"
    
    def total_item_price(self):
        return self.quantity * self.product.price
    
    def final_price(self):
        return self.total_item_price()
    
    
# Order
class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    items = models.ManyToManyField(OrderItem)
    ordered = models.BooleanField(default=False)
    ordered_date = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.user.username
    
    def total_price(self):
        total = 0
        for order_item in self.items.all():
            total += order_item.final_price()
        return total
    

# Address
class Address(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    address = models.TextField(null=False, blank=False)
    post_code = models.CharField(max_length=10, null=False, blank=False)
    
    def __str__(self):
        return self.user.username