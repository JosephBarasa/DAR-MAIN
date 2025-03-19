from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('home_artists/', views.home_artists, name='home_artists'),
    path('home_galleries/', views.home_galleries, name='home_galleries'),
    path('home_exhibitions/', views.home_exhibitions, name='home_exhibitions'),
    path('home_about/', views.home_about, name='home_about'),
    path('home_contact/', views.home_contact, name='home_contact')
]