# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('survey', '0007_auto_20150128_2115'),
    ]

    operations = [
        migrations.AddField(
            model_name='question',
            name='externalLink',
            field=models.CharField(blank=True, max_length=500, default=None, null=True),
            preserve_default=True,
        ),
    ]
