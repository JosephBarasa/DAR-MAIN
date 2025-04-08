from django.db import models
from django.conf import settings


class Events(models.Model):
    gallery = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)
    title = models.CharField(max_length=100, null=True)
    ticket_price = models.DecimalField(max_digits=8, decimal_places=2, null=True)  
    date_of_event = models.DateField(null=True)
    poster_image = models.ImageField(upload_to="event_posters", null=True)
    event_description = models.TextField(null=True)

    def __str__(self):
        return self.title
