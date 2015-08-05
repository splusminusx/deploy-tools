# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('release', '0003_release_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='release',
            name='status',
            field=models.CharField(choices=[('NW', 'New'), ('RD', 'Ready to deploy'), ('SC', 'Successful'), ('FL', 'Failed'), ('IP', 'Deploy in progress'), ('CN', 'Deploy canceled')], max_length=2, default='NW'),
        ),
    ]
