# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.validators
from django.conf import settings
import django.contrib.gis.db.models.fields
import jsonfield.fields


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='GravelSite',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
                ('name', models.CharField(max_length=80)),
                ('notes', models.TextField(default='', blank=True)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('date_modified', models.DateTimeField(auto_now=True)),
                ('geometry', django.contrib.gis.db.models.fields.MultiPolygonField(srid=3857)),
                ('shared_with_public', models.BooleanField(default=False)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='InputNode',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
                ('name', models.CharField(max_length=80)),
                ('notes', models.TextField(default='', blank=True)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('date_modified', models.DateTimeField(auto_now=True)),
                ('value', models.FloatField(validators=[django.core.validators.MinValueValidator(0.0), django.core.validators.MaxValueValidator(1.0)])),
                ('site', models.ForeignKey(to='survey.GravelSite')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='MapLayer',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
                ('name', models.CharField(max_length=200)),
                ('url_template', models.TextField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Pit',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
                ('name', models.CharField(max_length=80)),
                ('notes', models.TextField(default='', blank=True)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('date_modified', models.DateTimeField(auto_now=True)),
                ('geometry', django.contrib.gis.db.models.fields.PolygonField(srid=3857)),
                ('site', models.ForeignKey(to='survey.GravelSite')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
                ('name', models.CharField(max_length=80)),
                ('title', models.CharField(max_length=80)),
                ('question', models.CharField(max_length=250)),
                ('detail', models.TextField()),
                ('order', models.FloatField()),
                ('image', models.ImageField(upload_to='', blank=True)),
                ('supplement', models.FileField(upload_to='', blank=True)),
                ('choices', jsonfield.fields.JSONField(default='[\n        {\n          "choice": "high",\n          "value": 1.0\n        },\n        {\n          "choice": "low",\n          "value": 0.0\n        }\n]')),
                ('layers', models.ManyToManyField(blank=True, to='survey.MapLayer')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='inputnode',
            name='question',
            field=models.ForeignKey(to='survey.Question'),
            preserve_default=True,
        ),
        migrations.AlterUniqueTogether(
            name='inputnode',
            unique_together=set([('site', 'question', 'user')]),
        ),
    ]
