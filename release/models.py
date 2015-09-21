from django.contrib.auth.models import User
from django.db import models


DEFAULT_MAX_CHAR_FIELD_LENGTH = 256


class ArtifactType(models.Model):
    name = models.CharField(max_length=DEFAULT_MAX_CHAR_FIELD_LENGTH, blank=False, null=False)
    description = models.TextField(blank=True, null=False)

    class Meta:
        ordering = ('name', )

    def __str__(self):
        return self.name


class Environment(models.Model):
    name = models.CharField(max_length=DEFAULT_MAX_CHAR_FIELD_LENGTH, blank=False, null=False)
    description = models.TextField(blank=True, null=False)

    def __str__(self):
        return self.name


class Artifact(models.Model):
    type = models.ForeignKey(ArtifactType, blank=False, null=False)
    version = models.CharField(max_length=DEFAULT_MAX_CHAR_FIELD_LENGTH, blank=False, null=False)

    def __str__(self):
        return self.type.name + '@' + self.version

    def clean(self):
        if self.version:
            self.version = self.version.strip()

    class Meta:
        unique_together = ('type', 'version')


class Release(models.Model):
    NEW = 'NW'
    READY = 'RD'
    SUCCESSFUL = 'SC'
    FAILED = 'FL'
    IN_PROGRESS = 'IP'
    CANCELED = 'CN'
    RELEASE_STATUS = (
        (NEW, 'New'),
	(READY, 'Ready to deploy'),
	(SUCCESSFUL, 'Successful'),
	(FAILED, 'Failed'),
	(IN_PROGRESS, 'Deploy in progress'),
	(CANCELED, 'Deploy canceled')
    )

    name = models.CharField(max_length=DEFAULT_MAX_CHAR_FIELD_LENGTH, blank=False, null=False)
    manager = models.ForeignKey(User, blank=False, null=False)
    environment = models.ForeignKey(Environment, blank=False, null=False)
    start_time = models.DateTimeField(auto_now=False, auto_now_add=False, blank=False, null=False)
    end_time = models.DateTimeField(auto_now=False, auto_now_add=False, blank=False, null=False)
    artifacts = models.ManyToManyField(Artifact)
    description = models.TextField(blank=True, null=False)
    status = models.CharField(max_length=2, choices=RELEASE_STATUS, default=NEW)

    def __str__(self):
        return self.name

