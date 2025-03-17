from django.urls import path
from . import views


urlpatterns = [
    path('gallery_sign_up/', views.gallery_sign_up, name='gallery_sign_up'),
    path('gallery_sign_in/', views.gallery_sign_in, name='gallery_sign_in'),
    path('gallery_index/', views.gallery_index, name='gallery_index'),
    path('gallery_log_out/', views.gallery_sign_out, name='gallery_sign_out'),
]