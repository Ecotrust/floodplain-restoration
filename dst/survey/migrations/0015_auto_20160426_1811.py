# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('survey', '0014_auto_20160426_0135'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pitscoreweight',
            name='value',
            field=models.FloatField(null=True, blank=True, default=None, validators=[django.core.validators.MinValueValidator(0.0), django.core.validators.MaxValueValidator(1.0)]),
            preserve_default=True,
        ),
    ]
