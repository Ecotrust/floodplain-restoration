from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.views.generic import RedirectView
from survey import views
from django.conf import settings
import os

urlpatterns = patterns('',
    url(r'^api/', include('survey.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^accounts/', include('allauth.urls')),
    url(r'^silk/', include('silk.urls', namespace='silk')),
    url(r'^sessions/auth.js$', views.auth),
    url(r'^static/(?P<path>.*)$','django.views.static.serve',{'document_root': settings.STATIC_ROOT, 'show_indexes': True}),
    url(r'^app/bower_components/(?P<path>.*)$', 'django.views.static.serve',
        {'document_root': os.path.join(settings.APP_DIR, 'bower_components'),'show_indexes': False}),
    url(r'^app/(?P<path>.*)$', 'django.views.static.serve',
        {'document_root': os.path.join(settings.APP_DIR, 'app'),'show_indexes': False}),
    url(r'^$', RedirectView.as_view(url="/app/index.html")),
)
