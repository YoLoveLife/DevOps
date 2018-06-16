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
from utils.models import FILE
import uuid
__all__ = [
    'Work', 'Code_Work', 'Safety_Work',
]


class Work(models.Model):
    id = models.AutoField(primary_key=True)
    uuid = models.UUIDField(auto_created=True, default=uuid.uuid4, editable=False)
    info = models.TextField()

    class Meta:
        ordering = ['id', ]
        abstract = True


class Code_Work(Work):
    # 关联推出的任务
    user = models.ForeignKey(ExtendUser, default=None, blank=True, null=True, on_delete=models.SET_NULL)
    mission = models.ForeignKey(Mission, related_name='works', null=True, blank=True, on_delete=models.SET_NULL)
    push_mission = models.ForeignKey(Push_Mission, related_name='works', on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        permissions = (('yo_list_codework', u'罗列发布工单'),
                       ('yo_create_codework', u'新增发布工单'),
                       ('yo_detail_codework', u'详细查看发布工单'),
                       ('yo_exam_codework',u'审核发布工单'),
                       ('yo_run_codework',u'运行发布工单'),
                       ('yo_delete_codework', u'删除应用组'))


    @property
    def status(self):
        return self.push_mission.status

    @status.setter
    def status(self,status):
        self.push_mission.status = status
        self.push_mission.save()

    @property
    def vars_dict(self):
        from django.conf import settings
        dict = self.mission.vars_dict
        dict['BASE'] = settings.OPS_ROOT + str(self.uuid) + '/'
        dict['TOOL'] = settings.TOOL_ROOT + '/'
        if self.push_mission.files.count() !=0:
            for file in self.push_mission.files.all():
                dict[file.name] = settings.MEDIA_ROOT+'/'+file.file.name
        return dict

    @property
    def file_list(self):
        return self.mission.file_list

    @file_list.setter
    def file_list(self,file_list):
        fs =FILE.objects.filter(uuid__in=file_list)
        self.push_mission.files.set(fs)
        self.push_mission.status = 2
        self.push_mission.save()


class Safety_Work(Work):
    # 关联安全开启
    groups = models.ManyToManyField(Group, blank=True, related_name='works', verbose_name=_("works"))
