from django.urls import path
from . import views


urlpatterns = [
    path('gallery_sign_up/', views.gallery_sign_up, name='gallery_sign_up'),
    path('gallery_sign_in/', views.gallery_sign_in, name='gallery_sign_in'),
    path('gallery_index/', views.gallery_index, name='gallery_index'),
    path('gallery_log_out/', views.gallery_sign_out, name='gallery_sign_out'),
    path('gallery_artists/', views.gallery_artists, name='gallery_artists'),
    path('gallery_artworks/', views.gallery_artworks, name='gallery_artworks'),
    path('gallery_events/', views.gallery_events, name='gallery_events'),
    path('gallery_about/', views.gallery_about, name='gallery_about'),
    path('gallery_contact/', views.gallery_contact, name='gallery_contact'),
    path('gallery_dashboard/', views.gallery_dashboard, 
         name='gallery_dashboard'),
    path('gallery_artist_profile_display/<int:artist_id>/', 
         views.gallery_artist_profile_display, 
         name='gallery_artist_profile_display'),
    path('gallery_profile_edit/', views.gallery_profile_edit,
         name='gallery_profile_edit'),
    path('gallery_event_upload/', views.gallery_event_upload, 
         name='gallery_event_upload'),
]