# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('survey', '0012_pitscoreweight'),
    ]

    operations = [
        migrations.AddField(
            model_name='pitscoreweight',
            name='questionText',
            field=models.CharField(null=True, blank=True, default='', max_length=255),
            preserve_default=True,
        ),
    ]
