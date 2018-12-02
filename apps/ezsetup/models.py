# -*- coding:utf-8 -*-
# !/usr/bin/env python
# Time 18-7-3
# Author Yo
# Email YoLoveLife@outlook.com
from django.utils.translation import ugettext_lazy as _
from django.db import models
import uuid
from manager.models import Group,Host
from django.conf import settings

__all__ = [
    'SETUP',
]


class SETUP(models.Model):
    SETUP_TYPE = (
        (settings.TYPE_EZSETUP_MYSQL, 'MySQL'),
        (settings.TYPE_EZSETUP_REDIS, 'Redis'),
    )
    SETUP_STATUS= (
        (settings.STATUS_EZSETUP_DONE, '完成'),
        (settings.STATUS_EZSETUP_ERROR, '错误'),
        (settings.STATUS_EZSETUP_INSTALLING, '安装中'),
        (settings.STATUS_EZSETUP_UNREACHABLE, '机器不可达'),
        (settings.STATUS_EZSETUP_LACK_OF_KEY_OR_JUMPER, '缺少跳板机或密钥'),
    )
    id = models.AutoField(primary_key=True)
    uuid = models.UUIDField(auto_created=True, default=uuid.uuid4, editable=False)

    group = models.ForeignKey(Group, on_delete=models.SET_NULL, null=True, related_name='group_setup')
    hosts = models.ManyToManyField(Host, blank=True, related_name='host_setup', verbose_name=_("metas"))

    type = models.IntegerField(choices=SETUP_TYPE)
    create_time = models.DateTimeField(auto_now_add=True)
    finish_time = models.DateTimeField(auto_now=True)

    _status = models.IntegerField(choices=SETUP_STATUS, default=settings.STATUS_EZSETUP_INSTALLING)

    results = models.TextField()

    class Meta:
        permissions = (
            ('yo_list_setup', u'罗列数据库实例'),
            ('yo_create_setup', u'新增数据库实例')
        )

    @property
    def status(self):
        return self._status

    @status.setter
    def status(self, status):
        if not self._status < 0:
            self._status = status
            self.save()

    def results_append(self,results):
        self.results = self.results + str(results)
        self.save()
