# -*- coding: utf-8 -*-
# !/usr/bin/env python
# Time 18-1-18
# Author Yo
# Email YoLoveLife@outlook.com
from __future__ import unicode_literals
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.conf import settings
from ops.models import Push_Mission,Mission
from manager.models import Group,Host
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

"""
Check_Work
判断工单
由一个Mission组成其运行内容
关联一个Push_Mission记录其运行过程

"""
"""
Code_Work
流程工单
由一个Mission组成其运行内容 
关联一个Push_Mission记录其运行过程
"""
class Code_Work(Work):
    # 关联推出的任务
    user = models.ForeignKey(ExtendUser, default=None, blank=True, nulld=True, on_delete=models.SET_NULL)
    mission = models.ForeignKey(Mission, related_name='works', null=True, blank=True, on_delete=models.SET_NULL)
    push_mission = models.ForeignKey(Push_Mission, related_name='works', on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        permissions = (
            ('yo_list_codework', u'罗列发布工单'),
            ('yo_create_codework', u'新增发布工单'),
            ('yo_detail_codework', u'详细查看发布工单'),
            ('yo_exam_codework', u'审核发布工单'),
            ('yo_run_codework', u'运行发布工单'),
            ('yo_upload_codework', u'为工单上传文件'),
            ('yo_results_codework', u'查看错误工单信息'),
        )


    @property
    def status(self):
        return self.push_mission.status

    @property
    def vars_dict(self):
        from django.conf import settings
        dict = self.mission.vars_dict
        dict['BASE'] = settings.OPS_ROOT + '/' + str(self.uuid) + '/'
        dict['TOOL'] = settings.TOOL_ROOT + '/'
        if self.push_mission.files.count() != 0:
            for file in self.push_mission.files.all():
                dict[file.var_name] = settings.MEDIA_ROOT+'/'+file.file.name
        return dict

    @property
    def file_list(self):
        return self.mission.file_list

    @file_list.setter
    def file_list(self,file_list):
        fs =FILE.objects.filter(uuid__in=file_list)
        self.push_mission.files.set(fs)
        self.push_mission.status = settings.OPS_PUSH_MISSION_WAIT_RUN
        self.push_mission.save()


class Safe_Work(Work):
    SAFE_WORK_STATUS = (
        (settings.SAFEWORK_REJECT, '拒绝'),
        (settings.SAFEWORK_WAIT_RUN, '等待执行'),
        (settings.SAFEWORK_WAIT_DONE, '正在执行'),
        (settings.SAFEWORK_DONE, '执行完毕'),
    )
    _status = models.IntegerField(default=settings.SAFEWORK_WAIT_RUN, choices=SAFE_WORK_STATUS)

    # 来源
    src_group = models.OneToOneField(Group, related_name='src_safe_work', on_delete=models.SET_NULL, null=True, blank=True)
    src_hosts = models.ManyToManyField(Host,blank=True, related_name='src_safe_work', verbose_name=_("src_safe_work"))
    src_info = models.TextField()

    # 目标
    dest_group = models.OneToOneField(Group, related_name='dest_safe_work', on_delete=models.SET_NULL, null=True, blank=True)
    dest_hosts = models.ManyToManyField(Host, blank=True, related_name='dest_safe_work', verbose_name=_("dest_safe_work"))
    dest_port = models.IntegerField(default=0, null=True)
    dest_info = models.TextField()

    user = models.ForeignKey(ExtendUser, default=None, blank=True, null=True, on_delete=models.SET_NULL,
                             related_name='safe_work')
    executor = models.ForeignKey(ExtendUser, default=None, blank=True, null=True, on_delete=models.SET_NULL,
                                 related_name='exe_safe_work')


    class Meta:
        permissions = (
            ('yo_list_safework', u'罗列安全工单'),
            ('yo_create_safework', u'新增安全工单'),
            ('yo_status_safework', u'修改安全工单状态'),
            ('yo_detail_safework', u'详细查看安全工单')
        )

    @property
    def status(self):
        return self._status

    @status.setter
    def status(self, status):
        self._status = status