# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('release', '0002_auto_20150805_1053'),
    ]

    operations = [
        migrations.AddField(
            model_name='release',
            name='status',
            field=models.CharField(max_length=2, choices=[('NW', 'New'), ('RD', 'Ready to deploy'), ('SC', 'Successful'), ('FL', 'Failed'), ('IP', 'Deploy in progress')], default='NW'),
        ),
    ]
