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
import pdfkit



# Create your views here.
def export_pdf(request, pk):
    user = request.user
    try:
        site = Site.objects.get(user=user, id=pk)
        pits = Pit.objects.filter(site_id=pk, user_id=user.id)
    except:
        return False

    # pdf = generate_pdf(site, pits, user=user)
    pdf = generate_pdf(request, pk)
    response = HttpResponse(pdf, content_type="application/pdf")
    response['Content-Disposition'] = 'attachment; filename=%s_%s.%s' % (site.name, date.today().strftime("%Y_%m_%d"), 'pdf')
    response['Content-Length'] = len(pdf)
    return response

# def generate_pdf(site, pits, user):
def generate_pdf(request, pk):

    # Create pdf
    # packets = []
    # packet = BytesIO()

    outputStream = BytesIO()
    # reportPdfUrl = 'http://%s/app/index.html#/site/%s/report' % (request.META['HTTP_HOST'],str(pk))
    reportPdfUrl = 'http://www.google.com'
    reportPdfFile = '%s/download_%s.pdf' % (settings.STATIC_ROOT, pk)
    # conf = pdfkit.configuration(meta_tag_prefix="'CSRF_COOKIE': 'p8NNYXcOOqBAylgoZ30oqWUNthezwfdb'")

    # import ipdb
    # ipdb.set_trace()


    pdfkit.from_url(reportPdfUrl, outputStream)
    # pdfkit.from_url(reportPdfUrl, reportPdfFile)
    # pdfkit.from_url(reportPdfUrl, reportPdfFile, configuration=conf)

     #move to the beginning of the StringIO buffer
    # new_pdf = PdfFileMerger()
    # packet.seek(0)
    # new_pdf.append(packet)

    # new_pdf = PdfFileMerger('%s/download_%s.pdf' % (settings.STATIC_ROOT, pk))    

    # finally, return output
    # new_pdf.write(outputStream)

    final = outputStream.getvalue()
    outputStream.close()

    return final







    # # render a new PDF with Reportlab
    # can = canvas.Canvas(packet, pagesize=letter)
    # charLimit = 95
    # yValue = 730
    # xValue = 20
    # indent = [0, 20, 40, 60, 80, 100]
    # indentIndex = 0
    # can.setFont('Helvetica', 30)
    # can.drawString(xValue + indent[1], yValue, "Floodplain Gravel Mine Restoration")
    # yValue -= 35
    # can.drawString(xValue + indent[4], yValue, "Assessment Tool")
    # yValue -= 35
    # can.setFont('Helvetica', 25)
    # can.drawString(xValue + indent[1], yValue, "Site: %s" % site.name)

    # yValue -= 45




    # DEFAULT_WIDTH = 255
    # DEFAULT_HEIGHT = 255
    # DEFAULT_ZOOM = 6
    # MAX_ZOOM = 12
    # OVERVIEW_ZOOM = DEFAULT_ZOOM

    # (w_lng, s_lat, e_lng, n_lat) = site.geometry.extent
    # bbox = {
    #     'sw': {
    #         'lat': s_lat,
    #         'lng': w_lng
    #     },
    #     'ne': {
    #         'lat': n_lat,
    #         'lng': e_lng
    #     }
    # }

    # points = {
    #     'start_lat': s_lat,
    #     'start_lng': w_lng,
    #     'end_lat': n_lat,
    #     'end_lng': e_lng
    # }

    # zoom, center = get_zoom_center(bbox, DEFAULT_WIDTH, DEFAULT_HEIGHT)
    # if zoom == False:
    #     zoom = MAX_ZOOM
    # if zoom > 2:
    #     if zoom > MAX_ZOOM:
    #         zoom = MAX_ZOOM
    #     else:
    #         zoom = int(zoom - 1)
    # else:
    #     zoom = 2

    # # According to https://developers.google.com/maps/documentation/staticmaps/#api_key
    # # "Note that the use of a key is not required, though it is recommended."
    # # ... so we go without a key for simplicity
    # map_template = "http://maps.googleapis.com/maps/api/staticmap?center=" + str(center['lat']) + "," + str(center['lng']) + "&" \
    #           "maptype=terrain" \
    #           "&markers=color:red%%7C%(start_lat)f,%(start_lng)f%%7C%(end_lat)f,%(end_lng)f&sensor=false" 
    # detail_map = map_template % points + "&zoom=" + str(zoom) + "&size=" + str(DEFAULT_WIDTH) + "x" + str(DEFAULT_HEIGHT) #+ "&scale=2"
    # if zoom - 2 <= OVERVIEW_ZOOM:
    #     if zoom > 4:
    #         overzoom = zoom - 3
    #     else:
    #         overzoom = 2
    # else:
    #     overzoom = OVERVIEW_ZOOM
    # overview_map = map_template % points + "&zoom=" + str(overzoom) + "&size=" + str(DEFAULT_WIDTH) + "x" + str(DEFAULT_HEIGHT) #+ "&scale=2"






    # nodes = InputNode.objects.filter(site=site)
    # contexts = Context.objects.all().order_by('order')
    # for context in contexts:
    #     can.setFont('Helvetica', 22)
    #     can.drawString(xValue, yValue, "%s" % context.name)
    #     (yValue, can, packet, packets) = new_line(yValue, 30, can, packet, packets)
    #     categories = QuestionCategory.objects.filter(context=context).order_by('order')
    #     for category in categories:
    #         can.setFont('Helvetica', 16)
    #         can.drawString(xValue + indent[1], yValue, "%s" % category.name)
    #         (yValue, can, packet, packets) = new_line(yValue, 20, can, packet, packets)
    #         questions = Question.objects.filter(questionCategory=category)
    #         for question in questions:
    #             can.setFont('Helvetica', 12)
    #             index = 0
    #             while index < len(question.question):
    #                 if len(question.question) > index+charLimit:
    #                     lineText = ' '.join(question.question[index:(index+charLimit)].split(' ')[:-1])
    #                 else:
    #                     lineText = question.question[index:]
    #                 if index == 0:
    #                     can.drawString(xValue + indent[2], yValue, "%s" % lineText)
    #                 else:
    #                     can.drawString(xValue + indent[3], yValue, "%s" % lineText)
    #                 index += len(lineText)+1
    #                 (yValue, can, packet, packets) = new_line(yValue, 16, can, packet, packets)
    #             (yValue, can, packet, packets) = new_line(yValue, 6, can, packet, packets)
    #             node = nodes.get(question=question)
    #             answer = "No answer given."
    #             for choice in question.choices:
    #                 if choice['value'] == node.value:
    #                     answer = choice['choice']
    #             can.setFont('Helvetica', 14)
    #             index = 0
    #             ansCharLimit = charLimit - indent[2]
    #             while index < len(answer):
    #                 if len(answer) > index+ansCharLimit:
    #                     lineText = ' '.join(answer[index:(index+ansCharLimit)].split(' ')[:-1])
    #                 else:
    #                     lineText = answer[index:]
    #                 if index == 0:
    #                     can.drawString(xValue + indent[3], yValue, "%s" % lineText)
    #                 else:
    #                     can.drawString(xValue + indent[4], yValue, "%s" % lineText)
    #                 index += len(lineText)+1
    #                 (yValue, can, packet, packets) = new_line(yValue, 18, can, packet, packets)
    #             (yValue, can, packet, packets) = new_line(yValue, 4, can, packet, packets)


    #     (yValue, can, packet, packets) = new_line(yValue, 20, can, packet, packets)


    # can.save()
    # packets.append(packet)

    # #move to the beginning of the StringIO buffer
    # new_pdf = PdfFileMerger()
    # for packet in packets:
    #     packet.seek(0)
    #     new_pdf.append(packet)

    # # finally, return output
    # outputStream = BytesIO()
    # new_pdf.write(outputStream)

    # final = outputStream.getvalue()
    # outputStream.close()

    # return final

def new_line(y, delta, can, packet, packets):
    y -= delta
    if y <= 20:
        can.save()
        y = 750
        packets.append(packet)
        packet = BytesIO()
        can = canvas.Canvas(packet, pagesize=letter)
    return (y, can, packet, packets)

# def get_bounding_box(points):
#     y_vals = []
#     x_vals = []

#     for point in points:
#         if point[0] != None and point[1] != None:
#             y_vals.append(point[0])
#             if point[1] > 0:
#                 point[1] = point[1] - 360
#             x_vals.append(point[1])

#     bbox = {
#         'sw': {
#             'lat': min(y_vals),
#             'lng': min(x_vals)
#         },
#         'ne': {
#             'lat': max(y_vals),
#             'lng': max(x_vals)
#         }
#     }

#     return bbox

def get_zoom_center(bbox, width, height):
    import numpy        #TODO - use math instead

    center = {
        'lat': numpy.mean([bbox['sw']['lat'], bbox['ne']['lat']]),
        'lng': numpy.mean([bbox['sw']['lng'], bbox['ne']['lng']])
    }

    if center['lng'] < -180:
        center['lng'] = center['lng'] + 360

    x_range = abs(bbox['ne']['lng']-bbox['sw']['lng'])
    y_range = abs(bbox['ne']['lat']-bbox['sw']['lat'])
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
    

# # The below was taken from globalMapTiles.py:

# ###############################################################################
# # $Id$
# #
# # Project:  GDAL2Tiles, Google Summer of Code 2007 & 2008
# #           Global Map Tiles Classes
# # Purpose:  Convert a raster into TMS tiles, create KML SuperOverlay EPSG:4326,
# #           generate a simple HTML viewers based on Google Maps and OpenLayers
# # Author:   Klokan Petr Pridal, klokan at klokan dot cz
# # Web:      http://www.klokan.cz/projects/gdal2tiles/
# #
# ###############################################################################
# # Copyright (c) 2008 Klokan Petr Pridal. All rights reserved.
# #
# # Permission is hereby granted, free of charge, to any person obtaining a
# # copy of this software and associated documentation files (the "Software"),
# # to deal in the Software without restriction, including without limitation
# # the rights to use, copy, modify, merge, publish, distribute, sublicense,
# # and/or sell copies of the Software, and to permit persons to whom the
# # Software is furnished to do so, subject to the following conditions:
# #
# # The above copyright notice and this permission notice shall be included
# # in all copies or substantial portions of the Software.
# #
# # THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
# # OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# # FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL
# # THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# # LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
# # FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
# # DEALINGS IN THE SOFTWARE.
# ###############################################################################


# def latLonToMeters( lat, lon ):
#         "Converts given lat/lon in WGS84 Datum to XY in Spherical Mercator EPSG:900913"
#         import math
#         originShift = 2 * math.pi * 6378137 / 2.0

#         mx = lon * originShift / 180.0
#         my = math.log( math.tan((90 + lat) * math.pi / 360.0 )) / (math.pi / 180.0)

#         my = my * originShift / 180.0
#         return mx, my
