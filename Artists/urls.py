from django.urls import path
from . import views


urlpatterns = [
    path('artist_sign_up/', views.artist_sign_up, name='artist_sign_up'),
    path('artist_sign_in/', views.artist_sign_in, name='artist_sign_in'),
    path('artist_dashboard/', views.artist_dashboard, name='artist_dashboard')
]