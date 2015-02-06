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


    import xhtml2pdf.pisa as pisa

    html = """
    <!-- EWWW table based layout (plays nicer with pisa) -->
    <style>
      td {text-align: left; vertical-align:top}
      th {text-align: right; margin-right:20px}
      .map-frame {height: 255px; width: 255px}
    </style>

    <table>
      <tr>
        <td align="center" colspan="2">
           <h2> Floodplain Gravel Mine <br />Restoration Assessment Report </h2>
        </td>
      </tr>
      <tr>
        <td align="center" colspan="2">
           <h4> Site: %s </h2>
        </td>
      </tr>
      <tr>
        <td>
            <iframe class="map-frame" src="http://www.w3schools.com">
                <p>Your browser does not support iframes.</p>
            </iframe>
        </td>
        <td>
            <iframe class="map-frame" src="http://www.google.com">
                <p>Your browser does not support iframes.</p>
            </iframe>
        </td>
      </tr>
    </table>

    """ % (site.name)

    result = BytesIO()
    pdf = pisa.CreatePDF(html, result)
    
    if pdf.err:
        raise Exception("Pisa failed to create a pdf for observation")
    else:
        new_pdf = PdfFileReader(result)
        new_page = obs_pdf.getPage(0)
        return new_page


    # outputStream = BytesIO()
    # new_pdf.write(outputStream)

    # final = outputStream.getvalue()
    # outputStream.close()

    # return final










    # # Create pdf
    # packets = []
    # packet = BytesIO()

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

# def get_zoom_center(bbox, width, height):
#     import numpy        #TODO - use math instead

#     sw_x, sw_y = latLonToMeters(bbox['sw']['lat'], bbox['sw']['lng'])
#     sw_point = {
#         'lat': sw_y,
#         'lng': sw_x
#     }
#     ne_x, ne_y = latLonToMeters(bbox['sw']['lat'], bbox['ne']['lng'])
#     ne_point = {
#         'lat': ne_y,
#         'lng': ne_x
#     }

#     center = {
#         'lat': numpy.mean([bbox['sw']['lat'], bbox['ne']['lat']]),
#         'lng': numpy.mean([bbox['sw']['lng'], bbox['ne']['lng']])
#     }

#     if center['lng'] < -180:
#         center['lng'] = center['lng'] + 360

#     x_range = abs(ne_point['lng']-sw_point['lng'])
#     y_range = abs(ne_point['lat']-sw_point['lat'])
#     ratio = max(x_range/width, y_range/height)
#     zoom = get_zoom(center['lat'], ratio)

#     return zoom, center

# def get_zoom(lat, ratio):
#     import numpy        #TODO - use math instead
#     EARTH_CIRC = 6372798.2          # 6372.7982 km
#     rad_lat = numpy.radians(lat)
#     if ratio != 0 and EARTH_CIRC * numpy.cos(lat) != 0:
#         zoom = numpy.log2((EARTH_CIRC * numpy.cos(rad_lat))/ratio)-5
#     else:
#         return False 
#     return round(zoom)
    

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
