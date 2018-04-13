# -*- coding: utf-8 -*-
# !/usr/bin/env python
# Time 18-1-18
# Author Yo
# Email YoLoveLife@outlook.com
from __future__ import unicode_literals
from django.db import models
from django.utils.translation import ugettext_lazy as _
from ops.models import Push_Mission,Mission
from manager.models import Group
from authority.models import ExtendUser
import uuid
__all__ = [
    'Work', 'Code_Work', 'Safety_Work',
]


class Work(models.Model):
    id = models.AutoField(primary_key=True)
    uuid = models.UUIDField(auto_created=True, default=uuid.uuid4, editable=False)
    info = models.TextField()

    class Meta:
        ordering = ['id',]
        abstract = True


class Code_Work(Work):
    PROCESS_STATUS = (
        (0, u'未审核'),
        (1, u'文件上传'),
        (2, u'可执行'),
        (3, u'执行完毕'),
    )
    # 关联推出的任务
    user = models.ForeignKey(ExtendUser, default=None, blank=True, null=True)
    mission = models.ForeignKey(Mission, related_name='works', null=True, blank=True)
    push_mission = models.ForeignKey(Push_Mission, related_name='works', on_delete=models.SET_NULL, null=True, blank=True)
    status = models.IntegerField(choices=PROCESS_STATUS,default=0)

    class Meta:
        permissions = (('yo_list_codework', u'罗列发布工单'),
                       ('yo_create_codework', u'新增发布工单'),
                       ('yo_detail_codework', u'详细查看发布工单'),
                       ('yo_exam_codework',u'审核发布工单'),
                       ('yo_run_codework',u'运行发布工单'),
                       ('yo_delete_codework', u'删除应用组'))


class Safety_Work(Work):
    # 关联安全开启
    groups = models.ManyToManyField(Group, blank=True, related_name='works', verbose_name=_("works"))
