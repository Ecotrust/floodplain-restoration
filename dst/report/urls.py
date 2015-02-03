from django.conf.urls import *
from django.contrib import admin
from django.conf import settings
admin.autodiscover()

urlpatterns = patterns('',
    url('^export/(?P<pk>\d+)/$',
        'report.views.export_pdf'),
)
