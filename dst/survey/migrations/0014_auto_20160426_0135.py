# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('survey', '0013_pitscoreweight_questiontext'),
    ]

    operations = [
        migrations.CreateModel(
            name='PitQuestionAnswer',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('label', models.CharField(max_length=200)),
                ('value', models.FloatField(validators=[django.core.validators.MinValueValidator(0.0), django.core.validators.MaxValueValidator(1.0)])),
                ('pitQuestion', models.ForeignKey(to='survey.PitScoreWeight')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='pitscoreweight',
            name='info',
            field=models.CharField(max_length=255, blank=True, null=True, default=None),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='pitscoreweight',
            name='order',
            field=models.IntegerField(default=0),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='pitscoreweight',
            name='type',
            field=models.CharField(max_length=20, default='select', choices=[('text', 'Text'), ('select', 'Select'), ('textarea', 'Text Area')]),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='pitscoreweight',
            name='visible',
            field=models.BooleanField(default=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='pitscoreweight',
            name='score',
            field=models.CharField(max_length=30, primary_key=True, choices=[('name', 'Name'), ('contamination', 'Contamination'), ('adjacent_river_depth', 'Adj. River Depth'), ('slope_dist', 'Slope Distance'), ('pit_levies', 'Pit Levees'), ('bank_slope', 'Bank Slope'), ('surface_area', 'Surface Area'), ('notes', 'Notes')], serialize=False),
            preserve_default=True,
        ),
    ]
