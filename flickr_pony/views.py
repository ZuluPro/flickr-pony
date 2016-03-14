from django.shortcuts import render
from django.views.decorators.cache import cache_page
from django.conf import settings
from photos.storage import FlickrStorage


@cache_page(60*30)
def photos(request):
    storage = FlickrStorage(**settings.FLICKR_STORAGE_OPTIONS)
    photos = storage.list_image_and_thumb(size='m')
    return render(request, 'photos.html', {
        'photos': photos,
    })
