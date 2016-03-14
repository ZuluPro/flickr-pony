from django.conf.urls import include, url

urlpatterns = [
    url(r'^.*', 'ui.views.photos')
]
