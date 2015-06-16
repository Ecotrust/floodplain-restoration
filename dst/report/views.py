from django.http import HttpResponse, HttpResponseRedirect, HttpResponseBadRequest, HttpResponseServerError, HttpResponseForbidden
from django.template import RequestContext, loader
from django.core.exceptions import ObjectDoesNotExist
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
import math

def printer_friendly(request, pk, template_name='report/print.html'):
    user = request.user

    try:
        site = Site.objects.get(id=pk)
        if site.shared_with_public:
          pits = Pit.objects.filter(site_id=pk)
          answers = InputNode.objects.filter(site_id=pk)
        else:
          pits = Pit.objects.filter(site_id=pk, user_id=user.id)
          answers = InputNode.objects.filter(site_id=pk, user_id=user.id)
    except:
        return HttpResponseForbidden("<h1>ERROR 403 - Access Forbidden.</h1> <p>Are you logged in as the owner or is this site shared publicly?</p>")

    contexts = Context.objects.all().order_by('order')
    questions = Question.objects.all()
    question_map = []

    scores = {
        'suitability': {
            'key': 'Overall',
            'label': 'Overall'
        },
        'socio_economic': {
            'key': 'Socio-Economic',
            'label': 'Socio-Economic'
        },
        'site': {
            'key': 'Site',
            'label': 'Location'
        },
        'landscape': {
            'key': 'Landscape',
            'label': 'Landscape'
        }
    }

    pit_form = {
        'contamination': {
          'question': 'Is hazardous waste present?',
          'id': 'contamination',
          'answers': [
            {
              'label': 'I don\'t know',
              'value': 0.75
            },
            {
              'label': 'No, definitely not.',
              'value': 1
            },
            {
              'label': 'No, I don’t think so',
              'value': 0.8
            },
            {
              'label': 'Yes, and the cost and effort to remediate it is acceptable.',
              'value': 0.7
            },
            {
              'label': 'Yes, but I do not know if it can be remediated.',
              'value': 0.5
            },
            {
              'label': 'Yes, and it will be expensive and/or very difficult to remediate.',
              'value': 0.2
            }
          ]
        },
        'adjacent_river_depth': {
          'question': 'Is the pit deeper than the adjacent river <u><i>thalweg</i></u>?',
          'id': 'adjacent_river_depth',
          'answers': [
            {
              'label': 'I don\'t know',
              'value': 0.75
            },
            {
              'label': 'No',
              'value': 1
            },
            {
              'label': 'They are the same depth',
              'value': 0.9
            },
            {
              'label': 'Yes',
              'value': 0.5
            }
          ],
          'info': 'The thalweg of the river is the line of the lowest points within the channel, spanning the length of the river.'
        },
        'slope_dist': {
          'question': 'What is the distance from the river to the pit edge?',
          'id': 'slope_dist',
          'answers': [
            {
              'label': 'I don\'t know',
              'value': 0.9
            },
            {
              'label': 'Short (< 20 ft.)',
              'value': 1
            },
            {
              'label': 'Medium (20-80 ft.)',
              'value': 0.8
            },
            {
              'label': 'Long (> 80ft.)',
              'value': 0
            }
          ]
        },
        'pit_levies': {
          'question': 'Are there any pit-adjacent levees?',
          'id': 'pit_levies',
          'answers': [
            {
              'label': 'I don\'t know',
              'value': 0.85
            },
            {
              'label': 'No',
              'value': 1
            },
            {
              'label': 'Yes',
              'value': 0.7
            }
          ]
        },
        'bank_slope': {
          'question': 'Select the answer that best describes the slope of the pit bank:',
          'id': 'bank_slope',
          'answers': [
            {
              'label': 'I don\'t know',
              'value': 0.75
            },
            {
              'label': 'The bank slope is very shallow around most of the pit.',
              'value': 1
            },
            {
              'label': 'The bank slope is a mix of steep and shallow.',
              'value': 0.9
            },
            {
              'label': 'The bank slope is steep around most of the pit.',
              'value': 0.5
            }
          ]
        },
        'surface_area': {
          'question': 'What is the surface area of the pit?',
          'id': 'surface_area',
          'answers': [
            {
              'label': '< 5 acres',
              'value': 1
            },
            {
              'label': '5-20 acres',
              'value': 0.6
            },
            {
              'label': '20-30 acres',
              'value': 0.3
            },
            {
              'label': '> 30 acres',
              'value': 0
            }
          ]
        },
        'notes': {
          'question': 'Notes',
          'id': 'notes',
          'answers': []
        }
    }

    pit_scores = []
    for pit in pits:
        pit_score = {
            'id': pit.id,
            'contamination': {
                'question': pit_form['contamination']['question'],
                'answer': 'Answer not available',
                'value': pit.contamination
            },
            'adjacent_river_depth': {
                'question': pit_form['adjacent_river_depth']['question'],
                'answer': 'Answer not available',
                'value': pit.adjacent_river_depth
            },
            'slope_dist': {
                'question': pit_form['slope_dist']['question'],
                'answer': 'Answer not available',
                'value': pit.slope_dist
            },
            'pit_levies': {
                'question': pit_form['pit_levies']['question'],
                'answer': 'Answer not available',
                'value': pit.pit_levies
            },
            'bank_slope': {
                'question': pit_form['bank_slope']['question'],
                'answer': 'Answer not available',
                'value': pit.bank_slope
            },
            'surface_area': {
                'question': pit_form['surface_area']['question'],
                'answer': 'Answer not available',
                'value': pit.surface_area
            },
            'notes': {
                'question': pit_form['notes']['question'],
                'answer': pit.notes
            }
        }
        pit_score['score'] = 'Unsuitable'
        if pit.score > 0.33:
            pit_score['score'] = 'Moderately Suitable'
        if pit.score > 0.66:
            pit_score['score'] = 'Highly Suitable'
        for key, value in pit_form.items():
            if value['id'] != 'notes':
                for answer in value['answers']:
                    if answer['value'] == pit_score[value['id']]['value']:
                        pit_score[value['id']]['answer'] = answer['label']
                        break
        pit_scores.append(pit_score)
    for key, val in site.suitability.items():
        scores[key]['rank'] = 'Unsuitable'
        if val > 0.33:
            scores[key]['rank'] = 'Moderately Suitable'
        if val > 0.66:
            scores[key]['rank'] = 'Highly Suitable'

    for question in questions:
        answer_text = 'No answer available'
        try:
            answer = answers.get(question=question)
            for choice in question.choices:
                if choice['value'] == answer.value:
                    answer_text = choice['choice']
                    break
        except ObjectDoesNotExist:
            pass
        question_map.append({
            'question': question,
            'answer': answer_text
        })

    zoom = 13
    map_width = 300
    map_height = 300

    coords = site.geometry.envelope.coords
    north = coords[0][2][1]
    east = coords[0][1][0]
    south = coords[0][0][1]
    west = coords[0][0][0]
    height = math.fabs(north-south)
    width = math.fabs(west-east)
    size = math.sqrt((height*height)+(width*width))#in ~ meters... I think?

    if size < 3000:
        zoom=14
    elif size > 7000:
        zoom=12

    site.geometry.transform(4326)
    center = {
        'lat': site.geometry.centroid.get_y(),
        'lng': site.geometry.centroid.get_x()
    }

    point_str = ''
    pit_count = 0
    legend = []

    for pit in pits:
        pit_count += 1
        pit.geometry.transform(4326)
        lat = pit.geometry.centroid.get_y()
        lng = pit.geometry.centroid.get_x()
        point_str += '&markers=color:red%%7Clabel:%s%%7C%s,%s' % (str(pit_count), str(lat), str(lng))
        legend.append('<p>%s - %s</p>' % (pit_count, pit.name))

    overview_pt_str = '&markers=color:red%%7C%s,%s' % (str(center['lat']), str(center['lng']))

    map_template = "http://maps.googleapis.com/maps/api/staticmap?center=" + str(center['lat']) + "," + str(center['lng']) + "&" \
              "maptype=terrain&sensor=false"
    detail_map = map_template + point_str + "&zoom=" + str(zoom) + "&size=" + str(map_width) + "x" + str(map_height) #+ "&scale=2"
    overview_map = map_template + overview_pt_str + "&zoom=" + str(zoom-2) + "&size=" + str(map_width) + "x" + str(map_height) #+ "&scale=2"

    template = loader.get_template(template_name)

    context = RequestContext(
        request, {
            'site': site,
            'pits': pits,
            'pit_scores': pit_scores,
            'contexts': contexts.order_by('order'),
            'questions': question_map,
            'scores': scores,
            'map': detail_map,
            'overview': overview_map,
            'legend': legend
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

