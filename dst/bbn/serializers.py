from rest_framework import serializers
from rest_framework_gis.serializers import GeoFeatureModelSerializer
from bbn import models

class InputNodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.InputNode


class PitSerializer(GeoFeatureModelSerializer):
    class Meta:
        model = models.Pit
        geo_field = "geometry"


class GravelSiteSerializer(GeoFeatureModelSerializer):
    inputnode_set = InputNodeSerializer(many=True)
    pit_set = PitSerializer(many=True)
    class Meta:
        model = models.GravelSite
        geo_field = "geometry"


class MapLayerSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.MapLayer


class QuestionSerializer(serializers.ModelSerializer):
    def transform_choices(self, obj, value):
        return obj.choices  # represent as json, not string
    layers = MapLayerSerializer(many=True)
    class Meta:
        model = models.Question
