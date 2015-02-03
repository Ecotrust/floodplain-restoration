from django.shortcuts import render
from survey.models import GravelSite as Site
from survey.models import *
from django.http import HttpResponseForbidden, HttpResponse, \
                        HttpResponseBadRequest, Http404
from datetime import date, datetime

from reportlab.pdfgen import canvas
from PyPDF2 import PdfFileWriter, PdfFileReader, PdfFileMerger
from io import StringIO
from io import BytesIO
from reportlab.lib.pagesizes import letter
import os
import random
import datetime
from django.http import Http404
from django.conf import settings



# Create your views here.
def export_pdf(request, pk):
    user = request.user
    try:
        site = Site.objects.get(user=user, id=pk)
        pits = Pit.objects.filter(site_id=pk, user_id=user.id)
    except:
        return False

    pdf = generate_pdf(site, pits, user=user)
    response = HttpResponse(pdf, content_type="application/pdf")
    response['Content-Disposition'] = 'attachment; filename=%s_%s.%s' % (site.name, date.today().strftime("%Y_%m_%d"), 'pdf')
    response['Content-Length'] = len(pdf)
    return response

def generate_pdf(site, pits, user):
    # Create pdf
    packet = BytesIO()
    can = canvas.Canvas(packet)

    # render a new PDF with Reportlab
    can = canvas.Canvas(packet, pagesize=letter)
    can.setFont('Courier', 9)

    comment0 = "Please see additional notes in supporting documentation."
    can.drawString(110, 296, comment0)

    can.setFont('Courier', 7)
    disclaimer = "AWC nomination form generated by aklogbook.ecotrust.org"
    can.drawString(40, 215, disclaimer)
    can.setFont('Courier', 9)

    can.save()

    #move to the beginning of the StringIO buffer
    packet.seek(0)
    new_pdf = PdfFileMerger()
    new_pdf.append(packet)

    # finally, return output
    outputStream = BytesIO()
    new_pdf.write(outputStream)

    final = outputStream.getvalue()
    outputStream.close()

    return final

def get_bounding_box(points):
    y_vals = []
    x_vals = []

    for point in points:
        if point[0] != None and point[1] != None:
            y_vals.append(point[0])
            if point[1] > 0:
                point[1] = point[1] - 360
            x_vals.append(point[1])

    bbox = {
        'sw': {
            'lat': min(y_vals),
            'lng': min(x_vals)
        },
        'ne': {
            'lat': max(y_vals),
            'lng': max(x_vals)
        }
    }

    return bbox

def get_zoom_center(bbox, width, height):
    import numpy        #TODO - use math instead

    sw_x, sw_y = latLonToMeters(bbox['sw']['lat'], bbox['sw']['lng'])
    sw_point = {
        'lat': sw_y,
        'lng': sw_x
    }
    ne_x, ne_y = latLonToMeters(bbox['sw']['lat'], bbox['ne']['lng'])
    ne_point = {
        'lat': ne_y,
        'lng': ne_x
    }

    center = {
        'lat': numpy.mean([bbox['sw']['lat'], bbox['ne']['lat']]),
        'lng': numpy.mean([bbox['sw']['lng'], bbox['ne']['lng']])
    }

    if center['lng'] < -180:
        center['lng'] = center['lng'] + 360

    x_range = abs(ne_point['lng']-sw_point['lng'])
    y_range = abs(ne_point['lat']-sw_point['lat'])
    ratio = max(x_range/width, y_range/height)
    zoom = get_zoom(center['lat'], ratio)

    return zoom, center

def get_zoom(lat, ratio):
    import numpy        #TODO - use math instead
    EARTH_CIRC = 6372798.2          # 6372.7982 km
    rad_lat = numpy.radians(lat)
    if ratio != 0 and EARTH_CIRC * numpy.cos(lat) != 0:
        zoom = numpy.log2((EARTH_CIRC * numpy.cos(rad_lat))/ratio)-5
    else:
        return False 
    return round(zoom)
    

# The below was taken from globalMapTiles.py:

###############################################################################
# $Id$
#
# Project:  GDAL2Tiles, Google Summer of Code 2007 & 2008
#           Global Map Tiles Classes
# Purpose:  Convert a raster into TMS tiles, create KML SuperOverlay EPSG:4326,
#           generate a simple HTML viewers based on Google Maps and OpenLayers
# Author:   Klokan Petr Pridal, klokan at klokan dot cz
# Web:      http://www.klokan.cz/projects/gdal2tiles/
#
###############################################################################
# Copyright (c) 2008 Klokan Petr Pridal. All rights reserved.
#
# Permission is hereby granted, free of charge, to any person obtaining a
# copy of this software and associated documentation files (the "Software"),
# to deal in the Software without restriction, including without limitation
# the rights to use, copy, modify, merge, publish, distribute, sublicense,
# and/or sell copies of the Software, and to permit persons to whom the
# Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included
# in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
# OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL
# THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
# DEALINGS IN THE SOFTWARE.
###############################################################################


def latLonToMeters( lat, lon ):
        "Converts given lat/lon in WGS84 Datum to XY in Spherical Mercator EPSG:900913"
        import math
        originShift = 2 * math.pi * 6378137 / 2.0

        mx = lon * originShift / 180.0
        my = math.log( math.tan((90 + lat) * math.pi / 360.0 )) / (math.pi / 180.0)

        my = my * originShift / 180.0
        return mx, my
