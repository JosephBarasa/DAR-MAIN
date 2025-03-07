from django.shortcuts import render


def gallery_sign_up(request):
    return render(request, 'gallery/gallery_sign_up.html')


def gallery_sign_in(request):
    return render(request, 'gallery/gallery_sign_in.html')


def gallery_index(request):
    return render(request, 'gallery/gallery_index.html')