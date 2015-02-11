from django.http import HttpResponse, HttpResponseRedirect, HttpResponseBadRequest, HttpResponseServerError, HttpResponseForbidden
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

def view_pdf(request, filename=None, template_name='report/map.html', extra_context={}):

    if filename == None:
        filename = '22120150211222032'

    template = loader.get_template(template_name)

    context = RequestContext(
        request,{
            'js_file': '%s.js' % filename
        }
    )

    context.update(extra_context)
    return HttpResponse(template.render(context))

# Create your views here.
def export_pdf(request, pk=None):
    user = request.user
    try:
        site = Site.objects.get(user=user, id=pk)
        pits = Pit.objects.filter(site_id=pk, user_id=user.id)
    except:
        return HttpResponseForbidden("<h1>ERROR 403 - Access Forbidden.</h1> <p>Are you logged in?</p>")

    filename = '%s%s%s' % ( str(request.user.id), str(pk), datetime.datetime.now().strftime("%Y%m%d%H%M%S") )
    json_content = json.dumps({
        'site': json.dumps(site.geometry.geojson),
        'pits': json.dumps([json.dumps({'pk':x.pk,'name':x.name,'score':x.score,'geometry':x.geometry.geojson}) for x in pits])
    })

    js_content = 'requestJson = %s;' % (json_content)

    f = open('%s/%s.js' % (settings.STATIC_ROOT,filename), 'w')
    f.write(js_content)
    f.close()

    pdf = generate_pdf(request, site, filename)
    os.remove('%s/%s.js' % (settings.STATIC_ROOT,filename))
    response = HttpResponse(pdf, content_type="application/pdf")
    response['Content-Disposition'] = 'attachment; filename=%s_%s.%s' % (site.name, date.today().strftime("%Y_%m_%d"), 'pdf')
    response['Content-Length'] = len(pdf)
    return response

# def generate_pdf(site, pits, user):
def generate_pdf(request, site, filename):

    # reportPdfUrl = 'http://%s/report/view/%s' % (request.META['HTTP_HOST'],str(site.pk))
    reportPdfUrl = 'http://%s/report/view/%s' % (request.META['HTTP_HOST'],str(filename))

    outputStream = BytesIO()
    reportPdfFile = '%s/download_%s.pdf' % (settings.DOWNLOAD_ROOT, site.pk)

    wkhtmltopdfBinLocationString = '/usr/local/bin/wkhtmltopdf'
    wkhtmltopdfBinLocationBytes = wkhtmltopdfBinLocationString.encode('utf-8')
    config = pdfkit.configuration(wkhtmltopdf=wkhtmltopdfBinLocationBytes)

    print("url= %s ; file = %s" % (reportPdfUrl, reportPdfFile))
    pdfkit.from_url(reportPdfUrl, reportPdfFile, configuration=config, options={
        'javascript-delay': 1500,
        'load-error-handling': 'ignore'
    })

    new_pdf = PdfFileMerger()
    new_pdf.append('%s/download_%s.pdf' % (settings.DOWNLOAD_ROOT, site.pk))    

    # finally, return output
    new_pdf.write(outputStream)

    final = outputStream.getvalue()
    outputStream.close()
    os.remove(reportPdfFile)

    return final

