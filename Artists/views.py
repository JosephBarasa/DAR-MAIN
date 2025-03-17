from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.contrib.auth import authenticate, login, logout
from Users.models import CustomUser
from django.contrib.auth.decorators import login_required


def artist_sign_up(request):
    if request.method == 'POST':
        first_name = request.POST['firstname']
        last_name = request.POST['lastname']
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']
        
        # Email validation
        try:
            validate_email(email)
        except ValidationError:
            messages.error(request, 'Invalid email format!')
            return redirect('artist_sign_up')
        
        # Check if passwords match
        if password != confirm_password:
            messages.error(request, 'Passwords do not match!')
            return redirect('artist_sign_up')
        
        # Check if username exists
        if CustomUser.objects.filter(username=username).exists():
            messages.error(request, 'Username is taken!')
            return redirect('artist_sign_up')
        
        # Check if email exists
        if CustomUser.objects.filter(email=email).exists():
            messages.error(request, 'Email already exists!')
            return redirect('artist_sign_up')
        
        # Create and save artist
        user = CustomUser.objects.create_user(
            first_name=first_name, 
            last_name=last_name,
            username=username,
            email=email,
            password=password,
            role='artist',
        )
        user.save()
        
        messages.success(request, 'Your artist account has been created successfully!')
        return redirect('artist_sign_in')
        
    else:
        return render(request, 'artists/artist_sign_up.html')


def artist_sign_in(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            if user.role == 'artist':
                login(request, user)
                messages.success(request, 'Login Successful')
                return redirect('artist_index')
            else:
                messages.error(request, 'You are not registered as an artist.')
                return redirect('artist_sign_in')
        else:
            messages.error(request, 'Invalid username or password!')
            return redirect('artist_sign_in')
        
    return render(request, 'artists/artists_sign_in.html')


def artist_index(request):
    return render(request, 'artists/artist_index.html')


def artist_dashboard(request):
    return render(request, 'artists/artists_dashboard.html', {'user': request.user})


@login_required
def artist_profile_edit(request):
    user = request.user
    if request.method == 'POST':
        # Update fields from the form data
        user.first_name = request.POST.get('first_name', user.first_name)
        user.last_name = request.POST.get('last_name', user.last_name)
        user.residence = request.POST.get('residence', user.residence)
        user.bio = request.POST.get('bio', user.bio)
        
        # Handle file upload for profile picture if provided
        if 'profile_picture' in request.FILES:
            user.profile_picture = request.FILES['profile_picture']
        
        # Save updated user object
        user.save()
        messages.success(request, 'Your profile has been updated successfully.')
        return redirect('artist_dashboard')
    else:
        return render(request, 'artists/artist_profile_edit.html', {'user': user})


def artwork_upload(request):    
    return render(request, 'artists/artwork_upload.html')


def artist_sign_out(request):
    logout(request)
    return redirect('home')
