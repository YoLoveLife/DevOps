# -*- coding:utf-8 -*-
from __future__ import unicode_literals
from django.db import models
from django.conf import settings
import uuid


__all__ = [
    "CDN"
]


class CDN(models.Model):
    id = models.AutoField(primary_key=True)
    uuid = models.UUIDField(auto_created=True, default=uuid.uuid4, editable=False)

    url = models.CharField(max_length=1000, default='')
    status = models.IntegerField(default=settings.STATUS_CDN_RUN)
    create_time = models.DateTimeField(auto_now_add=True)
    type = models.IntegerField(default=settings.TYPE_CDN_ALIYUN)

    class Meta:
        permissions = (
            ('yo_yocdn_create', u'删除'),
        )