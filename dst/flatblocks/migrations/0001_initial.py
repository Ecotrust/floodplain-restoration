# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='FlatBlock',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('slug', models.CharField(unique=True, max_length=255, verbose_name='Slug', help_text='A unique name used for reference in the templates')),
                ('header', models.CharField(blank=True, max_length=255, verbose_name='Header', help_text='An optional header for this content')),
                ('content', models.TextField(blank=True, verbose_name='Content')),
            ],
            options={
                'verbose_name': 'Flat block',
                'verbose_name_plural': 'Flat blocks',
            },
            bases=(models.Model,),
        ),
    ]
