from django.contrib.auth.models import User
from django.db import models


DEFAULT_MAX_CHAR_FIELD_LENGTH = 256


class Service(models.Model):
    name = models.CharField(max_length=DEFAULT_MAX_CHAR_FIELD_LENGTH, blank=False, null=False)
    description = models.TextField(blank=True, null=False)

    def __str__(self):
        return self.name


class Environment(models.Model):
    name = models.CharField(max_length=DEFAULT_MAX_CHAR_FIELD_LENGTH, blank=False, null=False)
    description = models.TextField(blank=True, null=False)

    def __str__(self):
        return self.name


class Artifact(models.Model):
    service = models.ForeignKey(Service, blank=False, null=False)
    version = models.CharField(max_length=DEFAULT_MAX_CHAR_FIELD_LENGTH, blank=False, null=False)

    def __str__(self):
        return self.service.name + '@' + self.version


class Release(models.Model):
    name = models.CharField(max_length=DEFAULT_MAX_CHAR_FIELD_LENGTH, blank=False, null=False)
    manager = models.ForeignKey(User, blank=False, null=False)
    environment = models.ForeignKey(Environment, blank=False, null=False)
    start_time = models.DateTimeField(auto_now=False, auto_now_add=False, blank=False, null=False)
    end_time = models.DateTimeField(auto_now=False, auto_now_add=False, blank=False, null=False)
    artifacts = models.ManyToManyField(Artifact)
    description = models.TextField(blank=True, null=False)

    def __str__(self):
        return 'at ' + str(self.start_time) + ' to ' + self.environment.name
