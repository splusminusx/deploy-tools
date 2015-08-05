# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('release', '0001_initial'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='artifact',
            unique_together=set([('type', 'version')]),
        ),
    ]
