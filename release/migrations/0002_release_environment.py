# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('release', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='release',
            name='environment',
            field=models.ForeignKey(to='release.Environment', default=1),
            preserve_default=False,
        ),
    ]
