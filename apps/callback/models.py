# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from timeline.models import History
# Create your models here.

class Callback(models.Model):
    id = models.AutoField(primary_key=True)
    history = models.ForeignKey(History,default=1,related_name="callback")
    info = models.TextField()