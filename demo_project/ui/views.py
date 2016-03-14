"""Views for UI."""
from django.shortcuts import render
from django.views.decorators.cache import cache_page
from django.conf import settings
from flickr_pony.storage import FlickrStorage


@cache_page(60*30)
def photos(request):
    storage = FlickrStorage(**settings.FLICKR_STORAGE_OPTIONS)
    user_id = request.GET.get('user_id', '') or storage.user_id
    error = ''
    if user_id:
        try:
            photos = storage.list_image_and_thumb(user_id, size='m')
        except Exception as err:
            photos = []
            error = 'Error: %s' % err.args[0]
    else:
        photos = []
    return render(request, 'index.html', {
        'photos': photos,
        'user_id': user_id,
        'error': error
    })
