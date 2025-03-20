from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.contrib.auth import authenticate, login, logout
from .models import CustomUser

# USER SIGN UP


def user_sign_up(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']
        
        # email validation
        try:
            validate_email(email)
        except ValidationError:
            messages.error(request, 'Invalid email format!')
            return redirect('user_sign_up')
        
        # check if passwords match
        if password != confirm_password:
            messages.error(request, 'Passwords do not match!')
            return redirect('user_sign_up')
        
        # check if username already exists
        if CustomUser.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists!')
            return redirect('user_sign_up')
        
        # check if email already exists
        if CustomUser.objects.filter(email=email).exists():
            messages.error(request, 'Email already exists')
            return redirect('user_sign_up')
        
        # create and save the user in the db
        user = CustomUser.objects.create_user(username=username, email=email,
                                        password=password,
                                        role='normal_user')
        user.save()
        messages.success(request, 'Account created successfully.')
        return redirect('user_sign_in')
        
    else:
        return render(request, 'users/user_sign_up.html')
    

# USER SIGN IN


def user_sign_in(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            if user.role == 'normal_user':
                login(request, user)
                messages.success(request, 'Login Successful.')
                return redirect('user_index')
            else:
                messages.error(request, 'You are not registered as a normal user.')
                return redirect('user_sign_in')
        else:
            messages.error(request, 'Invalid username or password')
            return redirect('user_sign_in')
    else:
        return render(request, 'users/user_sign_in.html')


# USER SIGN OUT


def user_sign_out(request):
    logout(request)
    messages.success(request, 'You have been logged out successfully.')
    
    return redirect('home')


def user_index(request):
    return render(request, 'users/user_index.html')


def user_dashboard(request):
    return render(request, 'users/user_dashboard.html')


def user_profile_edit(request):
    return render(request, 'users/user_profile_edit.html')


def user_artists(request):
    artists = CustomUser.objects.filter(role='artist')
    return render(request, 'users/user_artists.html', {'artists': artists})
                  

def user_galleries(request):
    return render(request, 'users/user_galleries.html')


def user_events(request):
    return render(request, 'users/user_events.html')


def user_about(request):
    return render(request, 'users/user_about.html')


def user_contact(request):
    return render(request, 'users/user_contact.html')