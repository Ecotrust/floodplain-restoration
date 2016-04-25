# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('survey', '0011_bifsettings'),
    ]

    operations = [
        migrations.CreateModel(
            name='PitScoreWeight',
            fields=[
                ('score', models.CharField(choices=[('contamination', 'Contamination'), ('adjacent_river_depth', 'Adj. River Depth'), ('slope_dist', 'Slope Distance'), ('pit_levies', 'Pit Levies'), ('bank_slope', 'Bank Slope'), ('surface_area', 'Surface Area')], max_length=30, serialize=False, primary_key=True)),
                ('value', models.FloatField(validators=[django.core.validators.MinValueValidator(0.0), django.core.validators.MaxValueValidator(1.0)])),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
