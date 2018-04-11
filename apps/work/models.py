# -*- coding: utf-8 -*-
# !/usr/bin/env python
# Time 18-1-18
# Author Yo
# Email YoLoveLife@outlook.com
from __future__ import unicode_literals
from django.db import models
from django.utils.translation import ugettext_lazy as _
from ops.models import Push_Mission
from manager.models import Group
import uuid
__all__ = [
    'Work', 'Code_Work', 'Safety_Work',
]


class Work(models.Model):
    id = models.AutoField(primary_key=True)
    uuid = models.UUIDField(auto_created=True, default=uuid.uuid4, editable=False)

    class Meta:
        abstract = True


class Code_Work(Work):
    PROCESS_STATUS = (
        (0,u'未审核'),
        (1,u'文件上传'),
        (2,u'可执行')
    )
    # 关联推出的任务
    pushmission = models.ForeignKey(Push_Mission, related_name='works', on_delete=models.SET_NULL, null=True)
    status = models.IntegerField(choices=PROCESS_STATUS,default=0)


class Safety_Work(Work):
    # 关联安全开启
    groups = models.ManyToManyField(Group, blank=True, related_name='works', verbose_name=_("works"))
    info = models.TextField()