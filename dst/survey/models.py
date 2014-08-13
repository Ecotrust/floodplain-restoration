from django.contrib.gis.db import models
from django.contrib.auth.models import User
from django.conf import settings
from jsonfield import JSONField
from django.core.validators import MaxValueValidator, MinValueValidator
from silk.profiling.profiler import silk_profile #TODO remove


from bbn import BeliefNetwork
BBN = BeliefNetwork.from_bif(settings.BBN_BIF)


class BaseModel(models.Model):
    name = models.CharField(max_length=80)
    notes = models.TextField(default='', blank=True)
    user = models.ForeignKey(User)
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

    def __str__(self):   
        return "{} `{}` by {}".format(self.__class__.__name__,
                                      self.name,
                                      self.user.username)

class GravelSite(BaseModel):
    geometry = models.MultiPolygonField(srid=3857)
    objects = models.GeoManager()
    shared_with_public = models.BooleanField(default=False)

    @property
    def missing_questions(self):
        completed = [x.question.id for x in self.inputnode_set.all()]
        return Question.objects.exclude(id__in=completed)

    @property
    @silk_profile(name='Check Status')
    def status(self):
        status = {
            'missing_questions' : [x.id for x in self.missing_questions],
            'n_pits': len([x.id for x in self.pit_set.all()])
        }

        if len(status['missing_questions']) > 0 or status['n_pits'] == 0:
            status['complete'] = False
        else:
            status['complete'] = True

        return status

    @property
    @silk_profile(name='Check Suitability')
    def suitability(self):
        input_nodes = dict(
            [(x.question.name, 
                (BBN.variables[x.question.name][0], # assume first level is 1.0
                 x.value)) 
                for x in self.inputnode_set.all()])
        nodes_of_interest = (
            'suitability',
            'socio_economic',
            'site',
            'landscape',
        )
        output_nodes = [(x, BBN.variables[x][0]) for x in nodes_of_interest]
        vals = BBN.query(inputnodes=input_nodes, outputnodes=output_nodes)
        return dict(zip(nodes_of_interest, vals))


class Pit(BaseModel):
    site = models.ForeignKey(GravelSite)
    geometry = models.PolygonField(srid=3857)
    objects = models.GeoManager()


class MapLayer(models.Model):
    name = models.CharField(max_length=200)
    url_template = models.TextField()

    def __str__(self):
        return "Layer: {}".format(self.name)
 
class Question(models.Model):
    name = models.CharField(max_length=80)  # TODO slug correspond to the CPT
    title = models.CharField(max_length=80)
    question = models.CharField(max_length=250)
    detail = models.TextField()  # TODO HTML
    order = models.FloatField()

    # contextual info to help use answer the question
    image = models.ImageField(blank=True)
    supplement = models.FileField(blank=True)
    layers = models.ManyToManyField(MapLayer, blank=True, related_name="layers")
    
    # Many-To-Many with a through table is painful.
    # "The Django Way" for this problem sucks, just use a JSONField instead!
    # TODO Validate
    choices = JSONField(default="""[
        {
          "choice": "high",
          "value": 1.0
        },
        {
          "choice": "low",
          "value": 0.0
        }\n]""")

    @property
    def slug(self):
        return self.name.lower().replace(' ', "_").replace("-","_")

    def __str__(self):
        return "{}: `{}`".format(self.name, self.question)


class InputNode(BaseModel):
    site = models.ForeignKey(GravelSite)
    question = models.ForeignKey(Question)
    # (from BaseModel) 
    # `name` might be superfluous
    # `notes` might be useful
    value = models.FloatField(
        validators=[
            MinValueValidator(0.0),
            MaxValueValidator(1.0)
        ]
    )

    class Meta:
        unique_together = (('site', 'question', 'user'),)

    def __str__(self):   
        return "{} `{}` for {}".format(self.__class__.__name__,
                                      self.question.name,
                                      self.site.name)
