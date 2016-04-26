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

class BifSettings(BaseModel):
    bif = models.TextField(default='', blank=True)

    def __str__(self):
        return"{} by {}".format(self.__class__.__name__,
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


class PitScoreWeight(models.Model):
    PIT_FIELD_CHOICES = (
        ('name', 'Name'),
        ('contamination', 'Contamination'),
        ('adjacent_river_depth', 'Adj. River Depth'),
        ('slope_dist', 'Slope Distance'),
        ('pit_levies', 'Pit Levees'),
        ('bank_slope', 'Bank Slope'),
        ('surface_area', 'Surface Area'),
        ('notes', 'Notes'),
    )
    PIT_TYPE_CHOICES = (
        ('text', 'Text'),
        ('select', 'Select'),
        ('textarea', 'Text Area'),
    )
    score = models.CharField(primary_key=True, max_length=30, choices=PIT_FIELD_CHOICES)
    value = models.FloatField(validators=[MinValueValidator(0.0), MaxValueValidator(1.0)], blank=True, null=True, default=None)
    questionText = models.CharField(max_length=255, blank=True, null=True, default='')
    visible = models.BooleanField(default=True)
    order = models.IntegerField(default=0)
    type = models.CharField(max_length=20, choices=PIT_TYPE_CHOICES, default='select')
    info = models.CharField(max_length=255, blank=True, null=True, default=None)

class PitQuestionAnswer(models.Model):
    label = models.CharField(max_length=200)
    value = models.FloatField(validators=[MinValueValidator(0.0), MaxValueValidator(1.0)])
    pitQuestion = models.ForeignKey(PitScoreWeight)


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

        scoreMap = {}
        for score in attrs:
            scoreMap[score] = PitScoreWeight.objects.get(score=score).value

        # scoreMap = {
        # 'contamination': 0.8,
        # 'adjacent_river_depth': 0.33,
        # 'slope_dist': 0.42,
        # 'pit_levies': 0.03,
        # 'bank_slope': 0.05,
        # 'surface_area': 0.83
        # }

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
