# -*- coding:utf-8 -*-
from __future__ import unicode_literals
from django.db import models
from django.conf import settings
import uuid
from authority.models import ExtendUser


__all__ = [
    "Process"
]


class Process(models.Model):
    id = models.AutoField(primary_key=True)
    uuid = models.UUIDField(auto_created=True, default=uuid.uuid4, editable=False)

    url = models.CharField(max_length=1000, default='')
    user = models.ForeignKey(ExtendUser, default=None, blank=True, null=True, on_delete=models.SET_NULL)
    status = models.IntegerField(default=settings.STATUS_CDN_RUN)
    process = models.IntegerField(default=0)
    create_time = models.DateTimeField(auto_now_add=True)
    type = models.IntegerField(default=settings.TYPE_CDN_ALIYUN)

    class Meta:
        permissions = (
            ('yo_process_create', u'创建工序'),
            ('yo_process_update', u'更新工序'),
        )
