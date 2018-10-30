# -*- coding:utf-8 -*-
from __future__ import unicode_literals
from django.db import models
import uuid


__all__ = [
]


class Monitor(models.Model):
    id = models.AutoField(primary_key=True)
    uuid = models.UUIDField(auto_created=True, default=uuid.uuid4, editable=False)
    class Meta:
        permissions = (
            ('yo_monitor_aliyun', u'阿里云监控查看'),
            ('yo_monitor_vmware', u'VMware监控查看')
        )
