from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.contrib.auth import authenticate, login, logout
from .models import CustomUser
from Artworks.models import Artwork, Cart, CartItem, Order, OrderItem
from django.contrib.auth.decorators import login_required


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
    
    return redirect('home_index')


def user_index(request):
    return render(request, 'users/user_index.html')


def user_dashboard(request):
    return render(request, 'users/user_dashboard.html')


@login_required
def user_profile_edit(request):
    user = request.user
    if request.method == 'POST':
        user.first_name = request.POST['first_name']
        user.last_name = request.POST['last_name']
        user.residence = request.POST['residence']
        user.bio = request.POST['bio']
        
        # profile picture(file upload)
        if 'profile_picture' in request.FILES:
            user.profile_picture = request.FILES['profile_picture']
        
        user.save()
        messages.success(request, 'Your profile has been updated successfully.')
        return redirect('user_dashboard')
    
    else:
        return render(request, 'users/user_profile_edit.html')


def user_artists(request):
    artists = CustomUser.objects.filter(role='artist')
    return render(request, 'users/user_artists.html', {'artists': artists})
                  

def user_galleries(request):
    return render(request, 'users/user_galleries.html')


def user_artworks(request):
    artworks = Artwork.objects.all()
    return render(request, 'users/user_artworks.html', {'artworks': artworks})


def user_events(request):
    return render(request, 'users/user_events.html')


def user_about(request):
    return render(request, 'users/user_about.html')


def user_contact(request):
    return render(request, 'users/user_contact.html')


def user_artist_profile_display(request, artist_id):
    artist = get_object_or_404(CustomUser, id=artist_id, role='artist')
    artworks = Artwork.objects.filter(artist=artist)
    return render(request, 'users/artist_profile_display.html', {'artist': artist, 'artworks': artworks})


def artwork_view(request, artwork_id):
    artwork = get_object_or_404(Artwork, id=artwork_id)
    artist = artwork.artist
    return render(request, 'users/artwork_view.html', {'artwork': artwork,
                                                       'artist': artist})


@login_required
def add_to_cart(request, artwork_id):
    artwork = get_object_or_404(Artwork, id=artwork_id)
    
    # creating the user's cart
    cart, created = Cart.objects.get_or_create(user=request.user)
    
    # check if artwork exists in the cart
    cart_item, created = CartItem.objects.get_or_create(cart=cart, artwork=artwork)
    if not created:
        cart_item.quantity += 1
        cart_item.save()
    else:
        pass

    messages.success(request, f"{artwork.title} has been added to your cart.")
    return redirect('user_cart_view')

@login_required
def user_cart_view(request):
    cart = get_object_or_404(Cart, user=request.user)
    cart_items = CartItem.objects.filter(cart=cart)
    return render(request, 'users/user_cart_view.html', {'cart_items': cart_items})


@login_required
def remove_cart_item(request, artwork_id):
    
    # View to remove a specific item from the user's cart.

    # Handles both POST requests (for deletion) and GET requests
    # (for showing the deletion confirmation page).

    cart_item = get_object_or_404(CartItem, id=artwork_id)
    if request.method == 'POST':
        cart_item.delete()
        messages.success(request, 'Item removed from cart.')
        return redirect('user_cart_view')
    else:
        return render(request, 'users/user_cart_confirm_delete.html', {'cart_item': cart_item})


@login_required
def user_order_details(request, artwork_id):
    artwork = get_object_or_404(Artwork, id=artwork_id)
    if request.method == 'POST':
        from_shop = request.POST['from_shop']
        to = request.POST['to']
        phone_number = request.POST['phone_number']
        
        order = Order.objects.create(
            artwork=artwork,
            from_shop=from_shop,
            to=to,
            phone_number=phone_number,
        )

        order.save()
        
        messages.success(request, 'Your order has been placed, please proceed to make payment.')
        return redirect('mpesa_api')
    else:
        return render(request, 'users/user_order_details.html',
                  {'artwork': artwork})


def mpesa_api(request):
    return render(request, 'users/mpesa_api.html')
