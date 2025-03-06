from django.shortcuts import render


# HOME

def home(request):
    return render(request, 'home/index.html')


def artists(request):
    return render(request, 'home/artists.html')


def galleries(request):
    return render(request, 'home/gallery.html')


def exhibitions(request):
    return render(request, 'home/exhibitions.html')


def about(request):
    return render(request, 'home/about.html')


def contact(request):
    return render(request, 'home/contact.html')


