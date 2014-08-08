from rest_framework import serializers
from rest_framework_gis.serializers import GeoFeatureModelSerializer
from bbn.models import GravelSite, Pit, InputNode


class InputNodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = InputNode


class GravelSiteSerializer(GeoFeatureModelSerializer):
    class Meta:
        model = GravelSite
        geo_field = "geometry"


class PitSerializer(GeoFeatureModelSerializer):
    class Meta:
        model = Pit
        geo_field = "geometry"
