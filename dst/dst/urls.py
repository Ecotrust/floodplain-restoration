from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'dst.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^api/', include('bbn.urls')),
    url(r'^docs/', include('rest_framework_swagger.urls')),
    url(r'^admin/', include(admin.site.urls)),
)
