from django.conf.urls import *
from django.contrib import admin
from django.conf import settings
admin.autodiscover()

urlpatterns = patterns('',
    url('^export/(?P<pk>\d+)/$',
        'report.views.export_pdf'),
    url('^view/(?P<filename>\d+)',
        'report.views.view_pdf'),
    url('^view/$',
        'report.views.view_pdf'),
)
