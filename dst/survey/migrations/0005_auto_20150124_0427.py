# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('survey', '0004_auto_20150124_0236'),
    ]

    operations = [
        migrations.AddField(
            model_name='context',
            name='order',
            field=models.FloatField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='questioncategory',
            name='order',
            field=models.FloatField(default=0),
            preserve_default=False,
        ),
    ]
