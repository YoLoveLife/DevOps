# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
import uuid
# Create your models here.
class Softlib(models.Model):
    SOFT_CHOICES=(
        (0,u'no'),
        (1,u'Tomcat应用'),
        (2,u'数据库'),
        (3,u'redis缓存'),
        (4,u'nginx应用'),
        (5,u'rabbitmq队列'),
    )
    # id=models.AutoField(primary_key=True)
    id = models.UUIDField(auto_created=True, default=uuid.uuid4, editable=False, primary_key=True)
    soft_type = models.IntegerField(choices=SOFT_CHOICES,default=0)
    soft_version=models.CharField(max_length=10)
    # soft_md5=models.CharField(max_length=100,)