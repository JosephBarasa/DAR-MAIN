from django.shortcuts import render
from Users.models import CustomUser
from Artworks.models import Artwork


def home_index(request):
    return render(request, 'home/home_index.html')


def home_artists(request):
    artists = CustomUser.objects.filter(role='artist')
    return render(request, 'home/home_artists.html', {'artists': artists})


def home_galleries(request):
    return render(request, 'home/home_galleries.html')


def home_events(request):
    return render(request, 'home/home_events.html')


def home_artworks(request):
    artworks = Artwork.objects.all()
    return render(request, 'home/home_artworks.html', {'artworks': artworks})


def home_about(request):
    return render(request, 'home/home_about.html')


def home_contact(request):
    return render(request, 'home/home_contact.html')


