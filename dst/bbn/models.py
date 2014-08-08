from django.contrib.gis.db import models
from django.contrib.auth.models import User
from jsonfield import JSONField
from django.core.validators import MaxValueValidator, MinValueValidator

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
    def area(self):
        return self.geometry.area


class Pit(BaseModel):
    site = models.ForeignKey(GravelSite)
    geometry = models.PolygonField(srid=3857)
    objects = models.GeoManager()


class MapLayer(models.Model):
    name = models.CharField(max_length=200)
    url_template = models.TextField()

 
class Question(models.Model):
    name = models.CharField(max_length=80)  # TODO must correspond to the CPT
    title = models.CharField(max_length=80)
    question = models.CharField(max_length=250)
    detail = models.TextField()  # TODO HTML
    order = models.FloatField()

    # contextual info to help use answer the question
    image = models.ImageField(blank=True)
    supplement = models.FileField(blank=True)
    layers = models.ManyToManyField(MapLayer, blank=True)
    
    # Many-To-Many with a through table is painful.
    # "The Django Way" for this problem sucks, just use a JSONField instead!
    # TODO Validate
    choices = JSONField(default="""{
    "choices": [
        {
          "choice": "high",
          "value": 1.0
        },
        {
          "choice": "low",
          "value": 0.0
        }
    ]\n}""")

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

    def __str__(self):   
        return "{} `{}` for {}".format(self.__class__.__name__,
                                      self.question.name,
                                      self.site.name)
