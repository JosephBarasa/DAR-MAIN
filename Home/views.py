from django.shortcuts import render


def home(request):
    return render(request, 'home/index.html')


def home_artists(request):
    return render(request, 'home/artists.html')


def home_galleries(request):
    return render(request, 'home/gallery.html')


def home_exhibitions(request):
    return render(request, 'home/exhibitions.html')


def home_about(request):
    return render(request, 'home/about.html')


def home_contact(request):
    return render(request, 'home/contact.html')


