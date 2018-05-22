# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
# Create your models here.
class Callback(models.Model):
    id = models.AutoField(primary_key=True)
    info = models.TextField()