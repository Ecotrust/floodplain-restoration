# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('survey', '0015_auto_20160426_1811'),
    ]

    operations = [
        migrations.AddField(
            model_name='pitquestionanswer',
            name='default',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='pitquestionanswer',
            name='order',
            field=models.IntegerField(default=0),
            preserve_default=True,
        ),
    ]
