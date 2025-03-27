from django.urls import path
from . import views

urlpatterns = [
    path('home/', views.home_index, name='home_index'),
    path('home_artists/', views.home_artists, name='home_artists'),
    path('home_galleries/', views.home_galleries, name='home_galleries'),
    path('home_events/', views.home_events, name='home_events'),
    path('home_artworks/', views.home_artworks, name='home_artworks'),
    path('home_about/', views.home_about, name='home_about'),
    path('home_contact/', views.home_contact, name='home_contact')
]