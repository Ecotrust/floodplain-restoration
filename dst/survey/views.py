from rest_framework import viewsets
from rest_framework import renderers
from rest_framework import permissions
from rest_framework.decorators import link
from rest_framework.response import Response
from django.http import HttpResponse, HttpResponseForbidden

from survey.models import GravelSite, Pit, InputNode, Question
from survey import serializers
from survey.permissions import IsOwnerOrShared


class GravelSiteViewSet(viewsets.ModelViewSet):

    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.

    Additionally we also provide an extra `highlight` action.
    """
    #queryset = GravelSite.objects.all()
    model = GravelSite

    def get_queryset(self):
        return GravelSite.objects.filter(user=self.request.user)

    serializer_class = serializers.GravelSiteSerializer
    permission_classes = (
        permissions.IsAuthenticated,
        IsOwnerOrShared,
    )

    @link(renderer_classes=[renderers.JSONRenderer])
    def status(self, request, *args, **kwargs):
        obj = self.get_object()
        return Response(obj.status)

    @link(renderer_classes=[renderers.JSONRenderer])
    def suitability(self, request, *args, **kwargs):
        obj = self.get_object()
        return Response(obj.suitability)

    def pre_save(self, obj):
        obj.user = self.request.user


class PitViewSet(viewsets.ModelViewSet):

    """Pits """
    #queryset = Pit.objects.all()
    model = Pit

    def get_queryset(self):
        return Pit.objects.filter(user=self.request.user)

    serializer_class = serializers.PitSerializer
    permission_classes = (
        permissions.IsAuthenticated,
        IsOwnerOrShared,
    )

    def pre_save(self, obj):
        obj.user = self.request.user


class InputNodeViewSet(viewsets.ModelViewSet):

    """InputNode """
    #queryset = InputNode.objects.all()
    model = InputNode


    serializer_class = serializers.InputNodeSerializer
    permission_classes = (
        permissions.IsAuthenticated,
        IsOwnerOrShared,
    )

    def pre_save(self, obj):
        obj.user = self.request.user


class QuestionViewSet(viewsets.ReadOnlyModelViewSet):

    """Questions (Read only)"""
    queryset = Question.objects.all().order_by('order')
    serializer_class = serializers.QuestionSerializer


def auth(request):
    baseurl = request.get_host()
    username = None
    if request.user and request.user.is_authenticated():
        username = request.user.username

    template = """'use strict';
// Generated by django
angular
  .module('uiApp').run(function($rootScope){{
    $rootScope.userName = '{0}';
    $rootScope.baseUrl = '{1}'; // no trailing slash
  }});
    """

    if username:
        content = template.format(username, baseurl)
        return HttpResponse(content, status=200, content_type="application/javascript")
    else:
        content = template.format('', baseurl)
        return HttpResponseForbidden(content)
