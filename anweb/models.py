from __future__ import unicode_literals

from django.db import models

# Create your models here.
from django.db import models
class Soft(models.Model):
    id=models.IntegerField(primary_key=True)
    soft_name=models.CharField(max_length=100)
class Softlib(models.Model):
    id=models.IntegerField(primary_key=True,max_length=10)
    soft_type=models.ForeignKey(Soft)
    soft_version=models.CharField(max_length=10)
    soft_md5=models.CharField(max_length=100)


