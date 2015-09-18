# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations

lst = []


def populate_buf(apps, schema_editor):
    Release = apps.get_model('release', 'Release')
    for release in Release.objects.all():
        lst.append(release.environment)


def create_releases(apps, schema_editor):
    lst.reverse()
    Release = apps.get_model('release', 'Release')
    Environment = apps.get_model('release', 'Environment')

    for release in Release.objects.all():
        env = Environment.objects.get(name=lst.pop().name)
        release.environments.add(env)


class Migration(migrations.Migration):

    dependencies = [
        ('release', '0004_auto_20150805_2346'),
    ]

    operations = [
        migrations.RunPython(populate_buf),
        migrations.RemoveField(
            model_name='release',
            name='environment',
        ),
        migrations.AddField(
            model_name='release',
            name='environments',
            field=models.ManyToManyField(to='release.Environment'),
        ),
        migrations.RunPython(create_releases),
    ]