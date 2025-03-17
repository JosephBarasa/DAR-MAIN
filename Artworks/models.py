from django.db import models
from django.conf import settings


class Artwork(models.Model):
    artist = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,  null=True, related_name='artworks')
    title = models.CharField(max_length=255)
    image = models.ImageField(upload_to='artworks/')
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    year = models.IntegerField(default=0000)
    media = models.CharField(max_length=20, null=True)

    def __str__(self):
        return self.title
    
    
# class ArtworkSubmission(models.Model):
#     STATUS_CHOICES = [
#         ('pending', 'Pending'),
#         ('approved', 'Approved'),
#         ('rejected', 'Rejected'),
#     ]

#     artist = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,  null=True, related_name="submissions")
#     gallery = models.ForeignKey(Galleries, on_delete=models.CASCADE, related_name="submissions")
#     status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
#     submitted_at = models.DateTimeField(auto_now_add=True)
#     reviewed_at = models.DateTimeField(blank=True, null=True)

#     def __str__(self):
#         return f"{self.artist.username} -> {self.gallery.name} ({self.status})"

