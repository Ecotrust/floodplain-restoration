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

def printer_friendly(request, pk, template_name='report/print.html'):
    user = request.user
    try:
        site = Site.objects.get(user=user, id=pk)
        pits = Pit.objects.filter(site_id=pk, user_id=user.id)
        answers = InputNode.objects.filter(site_id=pk, user_id=user.id)
    except:
        return HttpResponseForbidden("<h1>ERROR 403 - Access Forbidden.</h1> <p>Are you logged in?</p>")

    contexts = Context.objects.all().order_by('order')
    questions = Question.objects.all()
    question_map = []

    for question in questions:
        answer = answers.get(question=question)
        answer_text = 'No answer available'
        for choice in question.choices:
            if choice['value'] == answer.value:
                answer_text = choice['choice']
                break
        question_map.append({
            'question': question,
            'answer': answer_text
        })

    # map site.suitability scores to contexts
    # return only site, contexts and pits

    template = loader.get_template(template_name)

    context = RequestContext(
        request, {
            'site': site,
            'pits': pits,
            'contexts': contexts.order_by('order'),
            'questions': question_map
        }
    )

    return HttpResponse(template.render(context))


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
            'pits': json.dumps([json.dumps({'pk':x.pk,'name':x.name,'score':x.score,'geometry':x.geometry.geojson}) for x in pits])
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
        return HttpResponseForbidden("<h1>ERROR 403 - Access Forbidden.</h1> <p>Are you logged in?</p>")

    pdf = generate_pdf(request, site)
    response = HttpResponse(pdf, content_type="application/pdf")
    response['Content-Disposition'] = 'attachment; filename=%s_%s.%s' % (site.name, date.today().strftime("%Y_%m_%d"), 'pdf')
    response['Content-Length'] = len(pdf)
    return response

# def generate_pdf(site, pits, user):
def generate_pdf(request, site):

    reportPdfUrl = 'http://%s/report/view/%s' % (request.META['HTTP_HOST'],str(site.pk))

    outputStream = BytesIO()
    reportPdfFile = '%s/download_%s.pdf' % (settings.DOWNLOAD_ROOT, site.pk)

    wkhtmltopdfBinLocationString = '/usr/local/bin/wkhtmltopdf'
    wkhtmltopdfBinLocationBytes = wkhtmltopdfBinLocationString.encode('utf-8')
    config = pdfkit.configuration(wkhtmltopdf=wkhtmltopdfBinLocationBytes)

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

