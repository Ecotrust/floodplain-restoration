from rest_framework import viewsets
from rest_framework import renderers
from rest_framework import permissions
from rest_framework.decorators import link
from rest_framework.response import Response
from django.http import HttpResponse, HttpResponseForbidden

from survey.models import GravelSite, Pit, InputNode, Question, Context, QuestionCategory
from survey import serializers
from survey.permissions import IsOwnerOrShared
from flatblocks.models import FlatBlock
from django.db.models import Q


class GravelSiteViewSet(viewsets.ModelViewSet):

    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.

    Additionally we also provide an extra `highlight` action.
    """
    #queryset = GravelSite.objects.all()
    model = GravelSite

    def get_queryset(self):
        if self.request.user.id:
            return GravelSite.objects.filter(Q(user=self.request.user) | Q(shared_with_public=True))
        else:
            return GravelSite.objects.filter(shared_with_public=True)
    serializer_class = serializers.GravelSiteSerializer
    permission_classes = (
        permissions.IsAuthenticatedOrReadOnly,
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
        if self.request.user.id:
            return Pit.objects.filter(Q(user=self.request.user) | Q(site__shared_with_public=True))
        else:
            return Pit.objects.filter(site__shared_with_public=True)

    serializer_class = serializers.PitSerializer
    permission_classes = (
        permissions.IsAuthenticatedOrReadOnly,
        IsOwnerOrShared,
    )

    def pre_save(self, obj):
        obj.user = self.request.user


class InputNodeViewSet(viewsets.ModelViewSet):

    """InputNode """
    model = InputNode
    filter_fields = ('site',)
    serializer_class = serializers.InputNodeSerializer
    permission_classes = (
        permissions.IsAuthenticatedOrReadOnly,
        IsOwnerOrShared,
    )

    def get_queryset(self):
        if self.request.user.id:
            return InputNode.objects.filter(Q(user=self.request.user) | Q(site__shared_with_public=True))
        else:
            return InputNode.objects.filter(site__shared_with_public=True)

    def pre_save(self, obj):
        obj.user = self.request.user


class QuestionViewSet(viewsets.ReadOnlyModelViewSet):

    """Questions (Read only)"""
    queryset = Question.objects.all().order_by('order')
    serializer_class = serializers.QuestionSerializer


class FlatblockSet(viewsets.ReadOnlyModelViewSet):

    """Flatblock (Read only)"""
    model = FlatBlock
    filter_fields = ('slug', 'header', 'content')
    queryset = FlatBlock.objects.all().order_by('header')
    serializer_class = serializers.FlatBlockSerializer


def auth(request):
    baseurl = request.get_host()
    username = None
    isadmin = False
    if request.user and request.user.is_authenticated():
        username = request.user.username
        if request.user.is_staff:
            isadmin = True

    template = """'use strict';
// Generated by django
angular
  .module('uiApp').run(function($rootScope){{
    $rootScope.userName = '{0}';
    $rootScope.baseUrl = '{1}'; // no trailing slash
    $rootScope.isAdmin = '{2}';
  }});
    """

    if username:
        content = template.format(username, baseurl, isadmin)
    else:
        content = template.format('', baseurl, isadmin)

    return HttpResponse(content, status=200, content_type="application/javascript")


class ContextSet(viewsets.ReadOnlyModelViewSet):
    """Contexts (Read only)"""
    model = Context
    filter_fields = ('name', 'order')
    queryset = Context.objects.all().order_by('order')
    serializer_class = serializers.ContextSerializer

class QuestionCategorySet(viewsets.ReadOnlyModelViewSet):
    """Question Categories (Read only)"""
    model = QuestionCategory
    filter_fields = ('name', 'context', 'order')
    queryset = QuestionCategory.objects.all().order_by('context__order', 'order')
    serializer_class = serializers.QuestionCategorySerializer

