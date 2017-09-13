# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.
class Softlib(models.Model):
    SOFT_CHOICES=(
        (0,u'no'),
        (1,u'tomcat'),
        (2,u'db'),
        (3,u'redis'),
        (4,u'nginx'),
        (5,u'rabbitmq'),
    )
    id=models.AutoField(primary_key=True)
    soft_type = models.CharField(max_length=100,choices=SOFT_CHOICES,default=0)
    soft_version=models.CharField(max_length=10)
    # soft_md5=models.CharField(max_length=100,)