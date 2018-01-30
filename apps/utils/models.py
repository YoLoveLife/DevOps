# -*- coding: utf-8 -*-
# !/usr/bin/env python
# Time 18-1-18
# Author Yo
# Email YoLoveLife@outlook.com

from __future__ import unicode_literals
from django.db import models
from manager.models import Group
import paramiko
from django.conf import settings
from deveops.utils import aes
from deveops.utils.msg import Message
from django.conf import settings
import socket


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

    @property
    def check_status(self):
        s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        s.settimeout(settings.SSH_TIMEOUT)
        try:
            s.connect((self.service_ip,self.sshport))
            return True
        except socket.timeout:
            return False
        except Exception,e:
            return False

    @property
    def catch_ssh_connect(self):
        msg = Message()
        if self.check_status == True:
            try:
                jumper = paramiko.SSHClient()
                jumper.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                jumper.connect(self.service_ip, username=self.normal_user,
                                  key_filename=settings.RSA_KEY, port=self.sshport,
                                  password=aes.decrypt(self.sshpasswd))
                return msg.fuse_msg('jumper-success',jumper)
            except socket.timeout:
                return msg.fuse_msg('jumper-timeout',None)
            except Exception,ex:
                return msg.fuse_msg('jumper-exception',None)
        else:
            return msg.fuse_msg('jumper-nocheck', None)