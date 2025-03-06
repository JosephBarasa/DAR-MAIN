from django.db import models
from django.contrib.auth.models import User


class Events(models.Model):
    name = models.CharField(max_length=100)
    date = models.DateField()

    def __str__(self):
        return self.name
    

class Galleries(models.Model):
    event = models.ForeignKey(Events, on_delete=models.CASCADE) 
    admin = models.ForeignKey(User, on_delete=models.CASCADE) 
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    

