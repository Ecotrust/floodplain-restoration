# from django.conf.urls.defaults import *
from django.conf.urls import patterns, url
from geosearch.views import *
# from django.conf import settings
# from django.views.generic.simple import redirect_to

urlpatterns = patterns(
    '',

    # Services
    url(r'search/$',
        search, name='placename'),
)
