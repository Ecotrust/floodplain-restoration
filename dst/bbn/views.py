from rest_framework import viewsets
from rest_framework import renderers
from rest_framework import permissions
from rest_framework.decorators import link
from rest_framework.response import Response

from bbn.models import GravelSite, Pit, InputNode, Question
from bbn import serializers
from bbn.permissions import IsOwnerOrShared


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

    @link(renderer_classes=[renderers.StaticHTMLRenderer])
    def area(self, request, *args, **kwargs):
        obj = self.get_object()
        return Response(obj.area)

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
    def get_queryset(self):
        return InputNode.objects.filter(user=self.request.user)

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
