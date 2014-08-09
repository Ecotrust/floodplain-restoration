# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import jsonfield.fields


class Migration(migrations.Migration):

    dependencies = [
        ('bbn', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='question',
            name='choices',
            field=jsonfield.fields.JSONField(default='[\n        {\n          "choice": "high",\n          "value": 1.0\n        },\n        {\n          "choice": "low",\n          "value": 0.0\n        }\n]'),
        ),
    ]
