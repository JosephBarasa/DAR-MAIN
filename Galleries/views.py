from django.shortcuts import render, redirect, get_object_or_404
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.contrib import messages
from Users.models import CustomUser
from django.contrib.auth import authenticate, login, logout
from Artworks.models import Artwork


def gallery_sign_up(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']
          
        try:
            validate_email(email)
        except ValidationError:
            messages.error(request, 'Invalid email format.')
            return redirect('gallery_sign_up')
        
        if CustomUser.objects.filter(username=username).exists():
            messages.error(request, 'Username taken.')
            return redirect('gallery_sign_up')
        
        if CustomUser.objects.filter(email=email).exists():
            messages.error(request, 'Email already exists.')
            return redirect('gallery_sign_up')
        
        if password != confirm_password:
            messages.error(request, 'Passwords do not match.')
            return redirect('gallery_sign_up')
        
        user = CustomUser.objects.create_user(
            username=username,
            email=email,
            password=password,
            role='gallery_admin',
        )
        user.save()
        messages.success(request, 'Gallery account successfully created.')
        return redirect('gallery_sign_in')
        
    return render(request, 'gallery/gallery_sign_up.html')


def gallery_sign_in(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            if user.role == 'gallery_admin':
                login(request, user)
                return redirect('gallery_index')
            else:
                messages.error(request, 'You are not registered as a Gallery Admin.')
                return redirect('gallery_sign_in')
        else:
            messages.error(request, 'Invalid username or password')
            return redirect('gallery_sign_in')
            
    return render(request, 'gallery/gallery_sign_in.html')


def gallery_index(request):
    return render(request, 'gallery/gallery_index.html')


def gallery_sign_out(request):
    logout(request)
    return redirect('home')


def gallery_artists(request):
    artists = CustomUser.objects.filter(role='artist')
    return render(request, 'gallery/gallery_artists.html', {'artists': artists})


def gallery_galleries(request):
    return render(request, 'gallery/gallery_galleries.html')


def gallery_events(request):
    return render(request, 'gallery/gallery_events.html')


def gallery_about(request):
    return render(request, 'gallery/gallery_about.html')


def gallery_contact(request):
    return render(request, 'gallery/gallery_contact.html')


def gallery_dashboard(request):
    return render(request, 'gallery/gallery_dashboard.html')


def gallery_artist_profile_display(request, artist_id):
    artist = get_object_or_404(CustomUser, id=artist_id, role='artist')
    artworks = Artwork.objects.filter(artist=artist)
    return render(request, 'gallery/artist_profile_display.html',
                  {'artist': artist, 'artworks': artworks })
