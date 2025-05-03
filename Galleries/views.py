from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.contrib import messages
from Users.models import CustomUser
from django.contrib.auth import authenticate, login, logout
from Artworks.models import Artwork
from django.contrib.auth.decorators import login_required
from Galleries.models import Events
from Artists.models import ArtworkSubmission


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
    return redirect('home_index')


def gallery_artists(request):
    artists = CustomUser.objects.filter(role='artist')
    return render(request, 'gallery/gallery_artists.html', {'artists': artists})


def gallery_artworks(request):
    return render(request, 'gallery/gallery_artworks.html')


def gallery_dashboard(request):
    gallery = request.user
    event = Events.objects.filter(gallery=request.user)
    artwork_submissions = ArtworkSubmission.objects.filter(gallery=gallery)
    return render(request, 'gallery/gallery_dashboard.html', 
                  {'event': event, 'gallery': gallery,
                   'artwork_submissions': artwork_submissions})


def gallery_artist_profile_display(request, artist_id):
    artist = get_object_or_404(CustomUser, id=artist_id, role='artist')
    artworks = Artwork.objects.filter(artist=artist)
    return render(request, 'gallery/artist_profile_display.html',
                  {'artist': artist, 'artworks': artworks })
    

@login_required
def gallery_profile_edit(request):
    user = request.user
    if request.method == 'POST':
        user.first_name = request.POST['first_name']
        user.residence = request.POST['residence']
        user.phone_number = request.POST['phone_number']
        user.email = request.POST['email']
        user.bio = request.POST['bio']
        
        if 'profile_picture' in request.FILES:
            user.profile_picture = request.FILES['profile_picture']
        
        user.save()
        messages.success(request, 'Your gallery profile has been successfully updated.')
        return redirect('gallery_dashboard')
    else:
        return render(request, 'gallery/gallery_profile_edit.html')


@login_required
def gallery_event_upload(request):
    
    gallery = request.user
    
    if request.method == 'POST':
        event_title = request.POST['title']
        date_of_event = request.POST['date_of_event']
        ticket_price = request.POST['ticket_price']
        event_description = request.POST['event_description']
        venue = request.POST.get('venue')
        if not venue:
            return HttpResponse("Venue is required.", status=400)
        
        if 'poster_image' in request.FILES:
            poster_image = request.FILES['poster_image']
            
        Events.objects.create(
            event_title=event_title,
            date_of_event=date_of_event,
            ticket_price=ticket_price,
            event_description=event_description,
            poster_image=poster_image,
            venue=venue,
            gallery=gallery
        )
        
        messages.success(request, 'Your event has been successfully uploaded.')
        return redirect('gallery_dashboard')
    
    else:
        return render(request, 'gallery/gallery_event_upload.html')


# NOTIFICATIONS
@login_required
def artwork_submissions(request):
    gallery = request.user
    artwork_submissions = ArtworkSubmission.objects.filter(gallery=gallery)
    return render(request, 'gallery/artwork_submissions.html', 
                  {'artwork_submissions': artwork_submissions})
    