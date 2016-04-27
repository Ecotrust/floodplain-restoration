# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('survey', '0016_auto_20160426_2303'),
    ]

    operations = [
        migrations.AddField(
            model_name='pitscoreweight',
            name='disabled',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
    ]
