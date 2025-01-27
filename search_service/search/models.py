from django.db import models

# Create your models here.

class Settings(models.Model):
    enabled = models.BooleanField(default=True)


class Fields(models.Model):
    model_name = models.CharField(max_length=32, blank=True)
    field_name = models.CharField(max_length=32, blank=True)
    field_type = models.CharField(max_length=50, blank=True)
    search_enabled = models.BooleanField(default=True)
    search_weight = models.FloatField(default=1, blank=True)

from django.db import models

# Create your models here.
