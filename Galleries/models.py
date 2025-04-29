from django.db import models
from django.conf import settings


class Events(models.Model):
    gallery = models.ForeignKey(settings.AUTH_USER_MODEL, 
                                on_delete=models.CASCADE, null=True)
    event_title = models.CharField(max_length=100, null=True)
    ticket_price = models.DecimalField(max_digits=8, decimal_places=2, 
                                       null=True)  
    date_of_event = models.DateField(null=True)
    poster_image = models.ImageField(upload_to="event_posters", null=True)
    venue = models.CharField(max_length=20, null=True)
    event_description = models.TextField(null=True)

    def __str__(self):
        return self.title


class Tickets(models.Model):
    event = models.ForeignKey(Events, on_delete=models.CASCADE, null=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, 
                             on_delete=models.CASCADE, null=True) 
    phone_number = models.IntegerField(null=True)
    amount = models.IntegerField(null=True)
    description = models.CharField(max_length=50, null=True)
    venue = models.CharField(max_length=20, null=True)
    date_of_event = models.DateField(null=True)
    status = models.CharField(max_length=15, default="Pending")
