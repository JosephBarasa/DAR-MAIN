from django.conf import settings
from django.db import models
from Artworks.models import Artwork


class ArtworkSubmission(models.Model):
    
    STATUS_PENDING = 'PENDING'
    STATUS_APPROVED = 'APPROVED'
    STATUS_REJECTED = 'REJECTED'
    STATUS_CHOICES = [
        (STATUS_PENDING, 'Pending Review'),
        (STATUS_APPROVED, 'Approved'),
        (STATUS_REJECTED, 'Rejected'),
    ]
    
    artwork = models.ForeignKey(Artwork, on_delete=models.CASCADE, null=True)
    artist = models.ForeignKey(settings.AUTH_USER_MODEL, 
                               on_delete=models.CASCADE, 
                               related_name='submissions')
    gallery = models.ForeignKey(settings.AUTH_USER_MODEL,
                                on_delete=models.CASCADE,
                                related_name='incoming_submissions')
    submitted_at = models.DateTimeField(auto_now_add=True, null=True)
    status = models.CharField(max_length=10,
                              choices=STATUS_CHOICES,
                              default=STATUS_PENDING)
    reviewed_at = models.DateTimeField(auto_now_add=True, null=True)
    rejection_note = models.TextField(blank=True)
    read = models.BooleanField(default=False)
    
    class Meta:
        unique_together = ('artwork', 'artist', 'gallery')
        
    def __str__(self):
        return f"{self.artwork.title} → {self.get_status_display()}"