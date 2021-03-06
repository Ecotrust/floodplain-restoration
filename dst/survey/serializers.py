from rest_framework import serializers
from rest_framework_gis.serializers import GeoFeatureModelSerializer
from survey import models
from flatblocks.models import FlatBlock


class InputNodeSerializer(serializers.ModelSerializer):
    user = serializers.IntegerField(read_only=True)

    class Meta:
        model = models.InputNode


class PitSerializer(GeoFeatureModelSerializer):

    def get_score(self, obj):
        pit_score = obj.score
        rank = "Highly Suitable"
        if pit_score < 0.33:
            rank = "Unsuitable"
        elif pit_score < 0.66:
            rank = "Moderately Suitable"
        return {
            'value': pit_score,
            'rank': rank
        }

    user = serializers.IntegerField(read_only=True)
    score = serializers.SerializerMethodField(method_name='get_score')

    class Meta:
        model = models.Pit
        geo_field = "geometry"


class GravelSiteSerializer(GeoFeatureModelSerializer):
    inputnode_set = InputNodeSerializer(many=True, read_only=True)
    pit_set = PitSerializer(many=True, read_only=True)
    user = serializers.IntegerField(read_only=True)

    class Meta:
        model = models.GravelSite
        geo_field = "geometry"


class MapLayerSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.MapLayer


class QuestionSerializer(serializers.ModelSerializer):

    def transform_choices(self, obj, value):
        return obj.choices  # represent as json, not string
    # layers = MapLayerSerializer(many=True)

    class Meta:
        model = models.Question

class FlatBlockSerializer(serializers.ModelSerializer):

    class Meta:
        model = FlatBlock

class ContextSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Context

class QuestionCategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = models.QuestionCategory

class PitQuestionAnswerSerializer(serializers.ModelSerializer):
    class Meta:
            model = models.PitQuestionAnswer
            fields = ('label', 'value', 'default', 'order')
            ordering_fields = ('order')
            ordering = ('order')

class PitScoreWeightSerializer(serializers.ModelSerializer):

    pitquestionanswer_set = PitQuestionAnswerSerializer(many=True)

    class Meta:
        model = models.PitScoreWeight
        fields = ('score','value','questionText','visible','disabled','order','type','info','pitquestionanswer_set')
