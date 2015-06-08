# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('survey', '0008_question_externallink'),
    ]

    operations = [
        migrations.AddField(
            model_name='question',
            name='impact',
            field=models.TextField(default=None, help_text='Explanation of how this issue impacts the score', blank=True, max_length=500, null=True),
            preserve_default=True,
        ),
    ]
