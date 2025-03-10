from django.shortcuts import render, redirect
from .forms import ProfileUpdateForm, ArtworkUploadForm
from .models import Profile
from django.contrib import messages


def artist_sign_up(request):
    return render(request, 'artists/artist_sign_up.html')


def artist_sign_in(request):
    return render(request, 'artists/artists_sign_in.html')


def artist_index(request):
    return render(request, 'artists/artist_index.html')


def artist_dashboard(request):
    # profile = Profile.objects.get(user=request.user)
    # artworks = request.user.artworks.all() 
    # return render(request, 'artists/artist_dashboard.html', {
    #     'profile': profile,
    #     'artworks': artworks
    # })
    return render(request, 'artists/artists_dashboard.html')


def artist_profile_edit(request):
    # profile = request.user.profile 
    # if request.method == 'POST':
    #     form = ProfileUpdateForm(request.POST, request.FILES, instance=profile)
    #     if form.is_valid():
    #         form.save()
    #         return redirect('artist_dashboard')
    # else:
    #     form = ProfileUpdateForm(instance=profile)
        
    return render(request, 'artists/artist_profile_edit.html')


def artwork_upload(request):
    # if request.method == 'POST':
    #     form = ArtworkUploadForm(request.POST, request.FILES)
    #     if form.is_valid():
    #         artwork = form.save(commit=False)
    #         artwork.artist = request.user 
    #         artwork.save()
    #         messages.success(request, 'Artwork uploaded successfully!')
    #         return redirect('artist_dashboard')
    # else:
    #     form = ArtworkUploadForm()
    
    return render(request, 'artists/artwork_upload.html', {'form': form})