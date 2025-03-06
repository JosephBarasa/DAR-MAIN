from django.db import models
from django.contrib.auth.models import User
from Artworks.models import Artwork


class Product(models.Model):
    artwork = models.OneToOneField(Artwork, on_delete=models.CASCADE, related_name='product')
    price = models.DecimalField(max_digits=12, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)
    is_available = models.BooleanField(default=True)
    
    def __str__(self):
        return f"{self.artwork.title} -${self.price}"
    
    
class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='cart')
    
    def total_cost(self):
        return sum(item.subtotal() for item in self.items.all())
    
    def __str__(self):
        return f"Cart ({self.user.username})"
    
    
class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='cart_item')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    
    def subtotal(self):
        return self.product.price * self.quantity
    
    def __str__(self):
        return f"{self.quantity} x {self.product.artwork.title}"
    
    
class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    created_at = models.DateTimeField(auto_now_add=True)
    total_price = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    status = models.CharField(
        max_length=20,
        choices=[('Pending', 'Pending'), ('Paid', 'Paid'), ('Shipped', 'Shipped'), ('Cancelled', 'Cancelled')],
        default='Pending'
    )
    
    def __str__(self):
        return f"Order {self.id} - {self.user.username} - {self.status}"