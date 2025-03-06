from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('artists/', views.artists, name='artists'),
    path('galleries/', views.galleries, name='galleries'),
    path('exhibitions/', views.exhibitions, name='exhibitions'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact')
]