from django.conf.urls import patterns, url
from django.contrib.admin.views.decorators import staff_member_required
from flatblocks.views import edit

urlpatterns = patterns('',
    url('^edit/(?P<pk>\d+)/$',
        staff_member_required(edit),
        name='flatblocks-edit'),
)
