# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('release', '0002_release_environment'),
    ]

    operations = [
        migrations.AddField(
            model_name='release',
            name='name',
            field=models.CharField(default='default', max_length=256),
            preserve_default=False,
        ),
    ]
