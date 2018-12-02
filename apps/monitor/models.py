# -*- coding:utf-8 -*-
# !/usr/bin/env python
# Time 18-3-19
# Author Yo
# Email YoLoveLife@outlook.com
from django.db import models
import uuid

__all__ = [
    'Monitor',
]


class Monitor(models.Model):
    id = models.AutoField(primary_key=True)
    uuid = models.UUIDField(auto_created=True, default=uuid.uuid4, editable=False)

    class Meta:
        permissions = (
            ('yo_monitor_aliyun', u'阿里云监控查看'),
            ('yo_monitor_vmware', u'VMware监控查看')
        )
