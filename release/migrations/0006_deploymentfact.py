# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('release', '0005_auto_20150918_1523'),
    ]

    operations = [
        migrations.CreateModel(
            name='DeploymentFact',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('status', models.CharField(choices=[('SC', 'Successful'), ('FL', 'Failed')], max_length=2, default='FL')),
                ('host', models.CharField(max_length=256)),
                ('datetime', models.DateTimeField(auto_now_add=True)),
                ('artifact', models.ForeignKey(to='release.Artifact')),
                ('environment', models.ForeignKey(to='release.Environment')),
            ],
        ),
    ]
