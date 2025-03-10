from django.urls import path
from . import views

urlpatterns = [
    path('user_index/', views.user_index, name='user_index'),
    path('user_sign_up/', views.user_sign_up, name='user_sign_up'),
    path('user_sign_in/', views.user_sign_in, name='user_sign_in'),
    path('user_sign_out/', views.user_sign_out, name='user_sign_out'),
    path('user_profile_display/', views.user_profile_display, name='user_profile_display'),
    path('user_profile_edit/', views.user_profile_edit, name='user_profile_edit'),
]