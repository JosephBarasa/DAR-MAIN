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


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='OrderItem')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    
    def subtotal(self):
        return self.price * self.quantity
    
    def __str__(self):
        return f"{self.order.id} - {self.product.artwork.title} ({self.quantity}x)"
    
    
class Payment(models.Model):
    order = models.OneToOneField(Order, on_delete=models.CASCADE,
                                 related_name='payment')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    payment_method = models.CharField(max_length=20,
                                      choices=[('Mpesa', 'Mpesa'), 
                                               ('Card', 'Card'), 
                                               ('Paypal', 'Paypal')])
    transaction_id = models.CharField(max_length=100, unique=True)
    status = models.CharField(
        max_length=20, choices=[('Pending', 'Pending'), 
                                ('Completed', 'Completed'), ('Failed', 'Failed')]
    )
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Payment {self.transaction_id} - {self.amount} {self.status}"
    
    
class LeasingAgreement(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, 
                             related_name='leases')
    artwork = models.ForeignKey(Artwork, on_delete=models.CASCADE, 
                                related_name='leases')
    start_date = models.DateField()
    end_date = models.DateField()
    price_per_month = models.DecimalField(max_digits=12, decimal_places=2)
    status = models.CharField(max_length=20, choices=[('Active', 'Active'), 
                                                      ('Completed', 'Completed'), ('Cancelled', 'Cancelled')])
    
    def total_cost(self):
        return f"{self.artwork.title} leased by {self.user.username}"