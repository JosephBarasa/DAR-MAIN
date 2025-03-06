from django.db import models
from django.contrib.auth.models import User
from Galleries.models import Events


class Tickets(models.Model):
    event = models.ForeignKey(Events, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity_available = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.name} - {self.event.name}"
    
    
class TicketOrder(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=[
        ('Pending', 'Pending'),
        ('Completed', 'Completed'),
        ('Cancelled', 'Cancelled')
    ])
    
    def __str__(self):
        return f"Order {self.id} by {self.user.username}"
    
    
class TicketOrderItem(models.Model):
    order = models.ForeignKey(TicketOrder, on_delete=models.CASCADE, related_name='items')
    ticket = models.ForeignKey(Tickets, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    
    def __str__(self):
        return f"{self.quantity} x {self.ticket.name} for {self.order.user.username}"
    