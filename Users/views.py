from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.contrib.auth import authenticate, login, logout
from .models import CustomUser
from Artworks.models import Artwork, Cart, CartItem, Order, MpesaPayment
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from .mpesa import MpesaClient
import json
from Galleries.models import Events, Tickets
# email
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from .pdf import generate_ticket_pdf

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


# user dashboard
def user_dashboard(request, user_id=None):
    # if you used user_id in the url
    if user_id:
        user = get_object_or_404(CustomUser, id=user_id)
    else:
        user = request.user
        
    # pull cart items and event tickets booked by the user
    cart_items = CartItem.objects.filter(cart__user=user)
    booked_tickets = Tickets.objects.filter(user=user, status='Pending')
    
    return render(request, 'users/user_dashboard.html', {
        'user': user,
        'cart_items': cart_items,
        'booked_tickets': booked_tickets,
    })


@login_required
def remove_cart_item(request, artwork_id):
    # fetch the user's cart
    user_cart = get_object_or_404(Cart, user=request.user)
    # Fetch the cart item using get_object_or_404
    cart_item = get_object_or_404(CartItem, artwork_id=artwork_id, 
                                  cart=user_cart)
    
    if request.method == 'POST':
        cart_item.delete()
        messages.success(request, 'Item removed from cart.')
        return redirect('user_dashboard')
    else:
        # Render a confirmation page with the cart item
        return render(request, 'users/user_cart_confirm_delete.html',
                      {'cart_item': cart_item})


@login_required
def user_profile_edit(request):
    user = request.user
    if request.method == 'POST':
        user.first_name = request.POST['first_name']
        user.last_name = request.POST['last_name']
        user.residence = request.POST['residence']
        user.bio = request.POST['bio']
        user.phone_number = request.POST['phone_number']
        
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
    galleries = CustomUser.objects.filter(role='gallery_admin')
    return render(request, 'users/user_galleries.html', 
                  {'galleries': galleries})


# display of artworks in the system

def user_artworks(request):
    artworks = Artwork.objects.all()
    return render(request, 'users/user_artworks.html', 
                  {'artworks': artworks})


# events and event tickets
def user_events(request):
    events = Events.objects.all()
    return render(request, 'users/user_events.html', {'events': events})


def get_event_ticket(request, event_id):
    event = get_object_or_404(Events, id=event_id)
    return render(request, 'users/get_event_ticket.html', {'event': event})


def user_about(request):
    return render(request, 'users/user_about.html')


def user_contact(request):
    return render(request, 'users/user_contact.html')


def user_artist_profile_display(request, artist_id):
    artist = get_object_or_404(CustomUser, id=artist_id, role='artist')
    artworks = Artwork.objects.filter(artist=artist)
    return render(request, 'users/artist_profile_display.html', 
                  {'artist': artist, 'artworks': artworks})


def user_gallery_dashboard_display(request, gallery_id):
    gallery = get_object_or_404(CustomUser, id=gallery_id,
                                role='gallery_admin')
    events = Events.objects.filter(gallery=gallery)
    return render(request, 'users/gallery_dashboard_display.html',
                  {'gallery': gallery,
                   'events': events})


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
    cart_item, created = CartItem.objects.get_or_create(cart=cart, 
                                                        artwork=artwork)
    if not created:
        cart_item.quantity += 1
        cart_item.save()
    else:
        pass

    messages.success(request, f"{artwork.title} has been added to your cart.")
    return redirect('user_dashboard')


# ORDERS
@login_required
def user_order_details(request, artwork_id):
    artwork = get_object_or_404(Artwork, id=artwork_id)
    artist = artwork.artist
    price = artwork.price
    
    if request.method == 'POST':
        from_shop = request.POST['from_shop']
        to = request.POST['to']
        phone_number = request.POST['phone_number']
        
        if Order.objects.filter(artwork=artwork).exists():
            messages.error(request, "Sorry, this artwork has been sold.")
            return redirect('artwork_view', artwork.id)
        
        order = Order.objects.create(
            user=request.user,
            artwork=artwork,
            from_shop=from_shop,
            to=to,
            phone_number=phone_number,
            total_price=price,
        )
        
        messages.success(request, 
                         'Your order has been placed, please proceed to make payment.')
        return redirect('mpesa_payment', order.id)
    else:
        return render(request, 'users/user_order_details.html',
                  {'artwork': artwork, 'artist': artist})


# MPESA API INTEGRATION


@login_required
def mpesa_payment(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    
    if request.method == 'POST':
        phone_number = request.POST.get('phone_number', order.phone_number)
        
        # Initialize M-Pesa client
        mpesa = MpesaClient()
        
        # Make STK push request
        response = mpesa.stk_push(
            phone_number=phone_number,
            amount=int(order.total_price),
            account_reference=f"ART-{order.id}",
            transaction_desc=f"Payment for {order.artwork.title}"
        )
        
        # Save the payment request to the database
        payment = MpesaPayment.objects.create(
            order=order,
            phone_number=phone_number,
            amount=order.total_price,
            reference=f"ART-{order.id}",
            description=f"Payment for {order.artwork.title}",
            request_id=response.get('CheckoutRequestID', ''),
            response=json.dumps(response)
        )
        
        # Check if the request was successful
        if response.get('ResponseCode') == '0':
            messages.success(request, 'Payment request sent. Please check your phone to complete the transaction.')
            return render(request, 'users/mpesa_payment_pending.html', {'order': order, 'payment': payment})
        else:
            messages.error(request, f"Payment request failed: {response.get('ResponseDescription', 'Unknown error')}")
            return redirect('user_order_details', order.artwork.id)
    else:
        return render(request, 'users/mpesa_payment.html', {'order': order})


@csrf_exempt
def mpesa_callback(request):
    """Handle the M-Pesa callback"""
    if request.method == 'POST':
        try:
            callback_data = json.loads(request.body)
            
            # Extract the callback data
            result_code = callback_data.get('Body', {}).get('stkCallback', {}).get('ResultCode')
            checkout_request_id = callback_data.get('Body', {}).get('stkCallback', {}).get('CheckoutRequestID')
            
            # Find the payment associated with this request
            try:
                payment = MpesaPayment.objects.get(request_id=checkout_request_id)
                
                # Update payment status
                if result_code == 0:  # 0 means success
                    payment.status = 'COMPLETED'
                    payment.completed_time = datetime.datetime.now()
                    payment.callback_data = json.dumps(callback_data)
                    payment.save()
                    
                    # Update order status
                    order = payment.order
                    order.payment_status = 'PAID'
                    order.save()
                else:
                    payment.status = 'FAILED'
                    payment.callback_data = json.dumps(callback_data)
                    payment.save()
                
                return JsonResponse({'ResultCode': 0, 'ResultDesc': 'Success'})
            except MpesaPayment.DoesNotExist:
                return JsonResponse({'ResultCode': 1, 'ResultDesc': 'Payment not found'})
                
        except Exception as e:
            return JsonResponse({'ResultCode': 1, 'ResultDesc': f'Error: {str(e)}'})
    
    return JsonResponse({'ResultCode': 1, 'ResultDesc': 'Invalid request method'})


# ticket payment

def ticket_payment(request, event_id):
    event = get_object_or_404(Events, id=event_id)
    if request.method == 'POST':
        phone_number = request.POST['phone_number']
        
        # initiate Mpesa-Client
        mpesa = MpesaClient()
        
        # make stk push request
        response = mpesa.stk_push(
            phone_number=phone_number,
            amount=int(event.ticket_price),
            account_reference=f"TICKET-{event.id}",
            transaction_desc=f"Payment for {event.event_title}"
        )
        
        # save payment request to the database
        ticket = Tickets.objects.create(
            event=event,
            phone_number=phone_number,
            amount=event.ticket_price,
            description=f"Ticket for {event.event_title}",
            user=request.user,
        )

        send_ticket_email(ticket)
        
        # check if request was successful
        if response.get('ResponseCode') == '0':
            messages.success(request, 'Payment request sent. Please check your phone to complete the transaction.')
            return render(request, 'users/ticket_payment_pending.html', {'event': event, 'ticket': ticket})
        else:
            messages.error(request, f"Payment request failed : {response.get('ResponseDescription', 'Unknown error')}")
            return redirect('ticket_payment', event.event.id)
    
    else:
        return render(request, 'users/ticket_payment.html', {'event': event})
    
# ticket email with pdf download


def send_ticket_email(ticket):
    user = ticket.user
     
    if not user or not user.email:
        raise ValueError("Ticket user or email is missing")
    
    # render a html email body
    subject = f"Your Ticket For {ticket.event.event_title}"
    body = render_to_string('emails/ticket_confirmation.html', {
        'ticket': ticket,
        'user': ticket.user,
        'event': ticket.event,
    })
    
    # create the email message
    email = EmailMessage(
        subject=subject,
        body=body,
        from_email=None,
        to=[user.email],
    )
    
    if not ticket.user:
        raise ValueError("Ticket has no associated user")
    
    email.content_subtype = 'html'
    
    # generate pdf and attach
    pdf_buffer = generate_ticket_pdf(ticket)
    email.attach(f"ticket_{ticket.id}.pdf", pdf_buffer.read(), 'application/pdf')
    
    # send
    email.send(fail_silently=False)
