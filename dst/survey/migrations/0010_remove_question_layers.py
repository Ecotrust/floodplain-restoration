# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('survey', '0009_question_impact'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='question',
            name='layers',
        ),
    ]
