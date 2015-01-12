# from django.shortcuts import render, render_to_response
from django.contrib.gis.geos import GEOSGeometry
from django.conf import settings
from django.http import HttpResponse, HttpResponseBadRequest
# from django.template import RequestContext
# from madrona.common.utils import get_logger
# from madrona.features.views import get_object_for_viewing
# from madrona.features import user_sharing_groups
from geopy import geocoders
from geopy.point import Point
# from trees.models import Stand
from django.views.decorators.cache import cache_page
# from django.core.cache import cache
import json
# import os

# Create your views here.

@cache_page(60 * 60 * 24 * 365)
def search(request):
    """
    Returns geocoded results in MERCATOR projection
    First tries coordinates, then a series of geocoding engines
    """
    from geopy import distance
    if request.method != 'GET':
        return HttpResponse('Invalid http method; use GET', status=405)

    try:
        txt = str(request.GET['search'])
    except:
        return HttpResponseBadRequest()

    searchtype = lat = lon = None
    place = txt
    try:
        p = Point(txt)
        lat, lon, altitude = p
        searchtype = 'coordinates'
    except:
        pass  # not a point

    centerloc = Point("45.54 N 120.64 W")
    max_dist = 315  # should be everything in WA and Oregon

    # import ipdb
    # ipdb.set_trace()
    searches = [
        geocoders.GeoNames('ecotrust','ecotrust'),
        geocoders.OpenMapQuest(), 
        # geocoders.Yahoo(app_id=settings.APP_NAME), 
        geocoders.Bing(api_key=settings.BING_API_KEY),
        # these are tried in reverse order, fastest first
        # TODO thread them and try them as they come in.
    ]

    while not (searchtype and lat and lon):  # try a geocoder
        try:
            g = searches.pop()
        except IndexError:
            break  # no more search engines left to try

        try:
            for p, loc in g.geocode(txt, exactly_one=False):
                d = distance.distance(loc, centerloc).miles
                if d < max_dist:
                    # TODO maybe compile these and return the closest to map center?
                    # print g, p, loc 
                    place = p
                    lat = loc[0]
                    lon = loc[1]
                    max_dist = d
                else:
                    pass
            searchtype = g.__class__.__name__
        except:
            pass

    if searchtype and lat and lon:  # we have a winner
        cntr = GEOSGeometry('SRID=4326;POINT(%f %f)' % (lon, lat))
        cntr.transform(settings.GEOMETRY_DB_SRID)
        cntrbuf = cntr.buffer(settings.POINT_BUFFER)
        extent = cntrbuf.extent
        loc = {
            'status': 'ok',
            'search': txt,
            'place': place,
            'type': searchtype,
            'extent': extent,
            'latlon': [lat, lon],
            'center': (cntr[0], cntr[1]),
        }
        json_loc = json.dumps(loc)
        return HttpResponse(json_loc, content_type='application/json', status=200)
    else:
        loc = {
            'status': 'failed',
            'search': txt,
            'type': None,
            'extent': None,
            'center': None,
        }
        json_loc = json.dumps(loc)
        return HttpResponse(json_loc, content_type='application/json', status=404)