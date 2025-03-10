from django.shortcuts import render


def artist_sign_up(request):
    return render(request, 'artists/artist_sign_up.html')


def artist_sign_in(request):
    return render(request, 'artists/artists_sign_in.html')


def artist_index(request):
    return render(request, 'artists/artist_index.html')


def artist_dashboard(request):
    return render(request, 'artists/artists_dashboard.html')


def artist_profile_edit(request):
    return render(request, 'artists/artist_profile_edit.html')


def artwork_upload(request):    
    return render(request, 'artists/artwork_upload.html', {'form': form})