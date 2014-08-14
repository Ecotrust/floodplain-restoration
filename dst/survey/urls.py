from django.conf.urls import patterns, url, include
from rest_framework.routers import DefaultRouter
from survey import views

# Create a router and register our viewsets with it.
router = DefaultRouter(trailing_slash=False)
router.register(r'site', views.GravelSiteViewSet)
router.register(r'pit', views.PitViewSet)
router.register(r'node', views.InputNodeViewSet)
router.register(r'questions', views.QuestionViewSet)

# The API URLs are now determined automatically by the router.
# Additionally, we include the login URLs for the browseable API.
urlpatterns = patterns('',
                       url(r'^', include(router.urls)),
                       #url(r'^auth/', include('rest_framework.urls', namespace='rest_framework'))
                       )
