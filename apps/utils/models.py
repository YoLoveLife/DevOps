# -*- coding: utf-8 -*-
# !/usr/bin/env python
# Time 18-1-18
# Author Yo
# Email YoLoveLife@outlook.com

from __future__ import unicode_literals

from django.db import models
from manager.models import Group


class Jumper(models.Model):
    SYSTEM_STATUS=(
        (0,'错误'),
        (1,'正常'),
        (2,'不可达'),
    )
    id=models.AutoField(primary_key=True) #全局ID
    service_ip = models.GenericIPAddressField(default='0.0.0.0')
    normal_user = models.CharField(max_length=15, default='')#普通用户
    sshpasswd = models.CharField(max_length=100,default='')#用户密码
    sshport = models.IntegerField(default='52000')#用户端口
    info = models.CharField(max_length=200,default="")
    groups = models.ManyToManyField(Group,null=True,related_name='jumpers')
    status = models.IntegerField(default=1,choices=SYSTEM_STATUS)#服务器状态

    def __unicode__(self):
        return self.service_ip + ' - ' + self.info