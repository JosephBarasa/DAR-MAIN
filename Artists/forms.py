from django import forms
from Artists.models import Profile
from Artworks.models import Artwork


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['profile_picture', 'first_name', 'last_name', 'bio', 'location']
        

class ArtworkUploadForm(forms.ModelForm):
    class Meta:
        model = Artwork
        fields = ['image', 'artist', 'title', 'price', 'year', 'description'] 