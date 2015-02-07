from django.http import HttpResponse #, HttpResponseRedirect, HttpResponseBadRequest, HttpResponseServerError, HttpResponseForbidden
from django.template import RequestContext, loader
# from django.shortcuts import get_object_or_404, render_to_response
# from django.utils import simplejson
import json

# from django.shortcuts import render
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

def view_pdf(request, pk, template_name='report/map.html', extra_context={}):

    if pk == '0':
        template = loader.get_template('report/test.html')
        context = RequestContext(
            request, {})
        context.update(extra_context)
        return HttpResponse(template.render(context))

    try:
        site = Site.objects.get(id=pk)
        pits = Pit.objects.filter(site_id=pk)
    except:
        return False

    template = loader.get_template(template_name)

    context = RequestContext(
        request,{
            'site': json.dumps(site.geometry.geojson),
            'pits': json.dumps([json.dumps(x.geometry.geojson) for x in pits])
        }
    )

    context.update(extra_context)
    return HttpResponse(template.render(context))

# Create your views here.
def export_pdf(request, pk):
    user = request.user
    try:
        site = Site.objects.get(user=user, id=pk)
        pits = Pit.objects.filter(site_id=pk, user_id=user.id)
    except:
        return False

    pdf = generate_pdf(request, site)
    response = HttpResponse(pdf, content_type="application/pdf")
    response['Content-Disposition'] = 'attachment; filename=%s_%s.%s' % (site.name, date.today().strftime("%Y_%m_%d"), 'pdf')
    response['Content-Length'] = len(pdf)
    return response

# def generate_pdf(site, pits, user):
def generate_pdf(request, site):

    reportPdfUrl = 'http://%s/report/view/%s' % (request.META['HTTP_HOST'],str(site.pk))
    testUrl = 'http://%s/report/view/0' % (request.META['HTTP_HOST'])
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
        <td align="center" colspan="2">
           <h4> Site: %s </h2>
        </td>
      </tr>
      <tr>
        <td>
            <iframe class="map-frame" src="%s">
                <p>Your browser does not support iframes.</p>
            </iframe>
        </td>
        <td>
            <!--
            <iframe class="map-frame" src="http://www.google.com">
                <p>Your browser does not support iframes.</p>
            </iframe>
            -->
        </td>
      </tr>
    </table>

    """ % (site.name, testUrl, reportPdfUrl)

    outputStream = BytesIO()
    reportPdfFile = '%s/download_%s.pdf' % (settings.DOWNLOAD_ROOT, site.pk)

    pdfkit.from_url(reportPdfUrl, reportPdfFile, options={
        'javascript-delay': 1000,
    })

    new_pdf = PdfFileMerger()
    new_pdf.append('%s/download_%s.pdf' % (settings.DOWNLOAD_ROOT, site.pk))    

    # finally, return output
    new_pdf.write(outputStream)

    final = outputStream.getvalue()
    outputStream.close()
    os.remove(reportPdfFile)

    return final

