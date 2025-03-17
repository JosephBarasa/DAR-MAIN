from django.contrib.auth.models import AbstractUser
from django.db import models
from configparser import MAX_INTERPOLATION_DEPTH

USER_ROLES = [
    ('artist', 'Artist'),
    ('gallery_admin', 'Gallery Administrator'),
    ('normal_user', 'Normal User'),
]


class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    role = models.CharField(max_length=20, choices=USER_ROLES, default='normal_user')
    profile_picture = models.ImageField(upload_to='profile_pictures/', null=True, blank=True)
    residence = models.CharField(max_length=20, null=True)
    bio = models.TextField(max_length=200, null=True)

    def __str__(self):
        return f"{self.username} ({self.role})"
