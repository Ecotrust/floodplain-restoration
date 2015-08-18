from django.contrib.gis.db import models
from django.contrib.auth.models import User
from django.conf import settings
from jsonfield import JSONField
from django.core.validators import MaxValueValidator, MinValueValidator


from bbn import BeliefNetwork
BBN = BeliefNetwork.from_bif(settings.BBN_BIF)


class BaseModel(models.Model):
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
    name = models.CharField(max_length=80)
    geometry = models.MultiPolygonField(srid=3857)
    objects = models.GeoManager()
    shared_with_public = models.BooleanField(default=False)

    @property
    def missing_questions(self):
        completed = [x.question.id for x in self.inputnode_set.all()]
        return Question.objects.exclude(id__in=completed)

    @property
    def status(self):
        status = {
            'missing_questions': [x.id for x in self.missing_questions],
            'n_pits': len([x.id for x in self.pit_set.all()])
        }

        if len(status['missing_questions']) > 0 or status['n_pits'] == 0:
            status['complete'] = False
        else:
            status['complete'] = True

        return status

    @property
    def suitability(self):
        input_nodes = dict(
            [(x.question.name,
                (BBN.variables[x.question.name][0],  # assume first level is 1.0
                 x.value))
                for x in self.inputnode_set.all()])

        # !! Assume Overall pit score is the weighted average of all pits
        total = sum(pit.score for pit in self.pit_set.all())
        numpits = self.pit_set.all().count()
        # !! Assume '__overall_pit_restorability' is the node of interest here
        pitnode = '__overall_pit_restorability'
        if numpits > 0:
            input_nodes[pitnode] = (BBN.variables[pitnode][0], total / numpits)

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
    name = models.CharField(max_length=80)
    site = models.ForeignKey(GravelSite)
    geometry = models.PolygonField(srid=3857)

    # Pit-specific attributes

    ## Water Quality Threat
    contamination = models.FloatField(validators=[MinValueValidator(0.0), MaxValueValidator(1.0)])

    ## Practical Restorability
    adjacent_river_depth = models.FloatField(validators=[MinValueValidator(0.0), MaxValueValidator(1.0)])
    slope_dist = models.FloatField(validators=[MinValueValidator(0.0), MaxValueValidator(1.0)])
    pit_levies = models.FloatField(validators=[MinValueValidator(0.0), MaxValueValidator(1.0)])

    ## Pit Geometry
    bank_slope = models.FloatField(validators=[MinValueValidator(0.0), MaxValueValidator(1.0)])
    surface_area = models.FloatField(validators=[MinValueValidator(0.0), MaxValueValidator(1.0)])

    ## Depricated
    bedrock = models.FloatField(blank=True, null=True, default=None, validators=[MinValueValidator(0.0), MaxValueValidator(1.0)])
    pit_depth = models.FloatField(blank=True, null=True, default=None, validators=[MinValueValidator(0.0), MaxValueValidator(1.0)])
    substrate = models.FloatField(blank=True, null=True, default=None, validators=[MinValueValidator(0.0), MaxValueValidator(1.0)])
    complexity = models.FloatField(blank=True, null=True, default=None, validators=[MinValueValidator(0.0), MaxValueValidator(1.0)])

    objects = models.GeoManager()

    @property
    def score(self):
        # TODO
        attrs = ['contamination', 'adjacent_river_depth',
                 'slope_dist', 'pit_levies', 'bank_slope',
                 'surface_area']


        scoreMap = {
        'contamination': 0.8,
        'adjacent_river_depth': 0.1,
        'slope_dist': 0.42,
        'pit_levies': 0.1,
        'bank_slope': 0.1,
        'surface_area': 0.8
        }

        total = 1
        for attr in attrs:
            total = total * (( self.__dict__[attr] * scoreMap[attr] ) + ( 1 - scoreMap[attr]))

        return total

    def __str__(self):
        return "Pit: {}".format(self.name)


class MapLayer(models.Model):
    name = models.CharField(max_length=200)
    url_template = models.TextField()

    def __str__(self):
        return "Layer: {}".format(self.name)

class Context(models.Model):
    name = models.CharField(max_length=250)
    order = models.FloatField()

    def __str__(self):
        return self.name

class QuestionCategory(models.Model):
    name = models.CharField(max_length=250)
    context = models.ForeignKey(Context)
    order = models.FloatField()

    def __str__(self):
        return self.name


class Question(models.Model):
    name = models.CharField(max_length=80)
    title = models.CharField(max_length=80)
    question = models.CharField(max_length=250)
    detail = models.TextField()
    order = models.FloatField()
    questionCategory = models.ForeignKey(QuestionCategory, blank=True, null=True, default=None)

    # contextual info to help use answer the question
    image = models.ImageField(blank=True)
    supplement = models.FileField(blank=True)
    externalLink = models.CharField(max_length=500, blank=True, null=True, default=None)
    # layers = models.ManyToManyField(
    #     MapLayer, blank=True, related_name="layers")
    impact = models.TextField(max_length=500, blank=True, null=True, default=None, help_text='Explanation of how this issue impacts the score')

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

    def __str__(self):
        return "{}: `{}`".format(self.name, self.question)

    def text(self):
        return self.question


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
