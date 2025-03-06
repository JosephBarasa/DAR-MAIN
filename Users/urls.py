from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('signin/', views.sign_in, name='sign_in'),
    path('signout/', views.sign_out, name='sign_out'),
    path('artist_profile_edit/', views.artist_profile_edit, name='artist_profile_edit'),
    path('artist_profile_display/', views.artist_profile_display, name='artist_profile_display'),
    path('artwork_upload/', views.artwork_upload, name='artwork_upload')
]