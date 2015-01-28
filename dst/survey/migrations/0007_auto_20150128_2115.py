# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('survey', '0006_remove_question_category'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pit',
            name='bedrock',
            field=models.FloatField(null=True, default=None, blank=True, validators=[django.core.validators.MinValueValidator(0.0), django.core.validators.MaxValueValidator(1.0)]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='pit',
            name='complexity',
            field=models.FloatField(null=True, default=None, blank=True, validators=[django.core.validators.MinValueValidator(0.0), django.core.validators.MaxValueValidator(1.0)]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='pit',
            name='pit_depth',
            field=models.FloatField(null=True, default=None, blank=True, validators=[django.core.validators.MinValueValidator(0.0), django.core.validators.MaxValueValidator(1.0)]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='pit',
            name='substrate',
            field=models.FloatField(null=True, default=None, blank=True, validators=[django.core.validators.MinValueValidator(0.0), django.core.validators.MaxValueValidator(1.0)]),
            preserve_default=True,
        ),
    ]
