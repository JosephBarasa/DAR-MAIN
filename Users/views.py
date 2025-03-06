from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.urls import reverse 
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .forms import ProfileUpdateForm, ArtworkUploadForm
from .models import Profile


def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        
        # Check if username already exists
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username is taken!')
            return redirect(reverse('register'))
        
        # Check if passwords match
        if password1 != password2:
            messages.error(request, 'Passwords do not match!')
            return redirect(reverse('register'))  

        # Check if email already exists
        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email already exists!')
            return redirect(reverse('register'))

        # Create the user if there are no validation issues
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password1
        )
        
        user.is_active = True 
        user.save()  
        
        # Display success message
        messages.success(request, f'Hello {username}, your account has been successfully created!')
        return redirect(reverse('sign_in'))  # Redirect to login page

    return render(request, 'users/register.html')


def sign_in(request):
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '').strip()

        if not username or not password:
            messages.error(request, 'Username and password are required!')
            return redirect('sign_in')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            # Ensure the user has a profile
            Profile.objects.get_or_create(user=user)
            return redirect('/') 
        else:
            messages.error(request, 'Invalid credentials!')
            return redirect('sign_in')

    return render(request, 'users/sign_in.html')


def sign_out(request):
    logout(request)
    return redirect('/')


@login_required
def artist_profile_edit(request):
    profile = request.user.profile 
    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('artist_profile_display')
    else:
        form = ProfileUpdateForm(instance=profile)
        
    return render(request, 'users/artist_profile_edit.html', {'form': form})


# ARTWORK UPLOAD

@login_required
def artist_profile_display(request):
    profile = Profile.objects.get(user=request.user)
    artworks = request.user.artworks.all()  
    
    return render(request, 'users/artist_profile_display.html', {
        'profile': profile,
        'artworks': artworks
    })
    
    
@login_required
def artwork_upload(request):
    if request.method == 'POST':
        form = ArtworkUploadForm(request.POST, request.FILES)
        if form.is_valid():
            artwork = form.save(commit=False)
            artwork.artist = request.user 
            artwork.save()
            messages.success(request, 'Artwork uploaded successfully!')
            return redirect('artist_profile_display')
    else:
        form = ArtworkUploadForm()
    
    return render(request, 'users/artwork_upload.html', {'form': form})
