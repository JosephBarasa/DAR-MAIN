from django.urls import path
from . import views


urlpatterns = [
    path('artist_sign_up/', views.artist_sign_up, name='artist_sign_up'),
    path('artist_sign_in/', views.artist_sign_in, name='artist_sign_in'),
    path('artist_index/', views.artist_index, name='artist_index'),
    path('artist_dashboard/', views.artist_dashboard, name='artist_dashboard'),
    path('artist_profile_edit/', views.artist_profile_edit, name='artist_profile_edit'),
    path('artwork_upload/', views.artwork_upload, name='artwork_upload'),
    path('artwork_edit/<int:artwork_id>/', views.artwork_edit, name='artwork_edit'),
    path('artwork/<int:artwork_id>/delete/', views.artwork_delete, name='artwork_delete'),
    path('artist_sign_out/', views.artist_sign_out, name='artist_sign_out'),
    path('artist_artists/', views.artist_artists, name='artist_artists'),
    path('artist_galleries/', views.artist_galleries, name='artist_galleries'),
    path('artist_artworks/', views.artist_artworks, name='artist_artworks'),
    path('artist_events/', views.artist_events, name='artist_events'),
    path('artist_profile_display/<int:artist_id>/',
         views.artist_profile_display, name='artist_profile_display'),
    path('submit_artwork_to_gallery/<int:artwork_id>/<int:gallery_id>/', 
         views.submit_artwork_to_gallery, name='submit_artwork_to_gallery'),
    path('artwork_approvals/', views.artwork_approvals, 
         name='artwork_approvals'),
    path('artwork_approvals/<int:submission_id>/', 
         views.mark_approval_as_read, name='mark_approval_as_read'),
]