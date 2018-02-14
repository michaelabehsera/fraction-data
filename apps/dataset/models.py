from django.db import models
from django.contrib.postgres.fields import JSONField
from django.conf import settings


class DataSet(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='datasets')
    name = models.CharField('DataSet Name', max_length=64, unique=True)
    description = models.TextField('DataSet Description', blank=True)

    column_names = JSONField(null=True, blank=True)
    data = JSONField(null=True, blank=True)

    def __str__(self):
        return self.name

