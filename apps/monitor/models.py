# -*- coding:utf-8 -*-
from __future__ import unicode_literals
from django.utils.translation import ugettext_lazy as _
from django.db import models
from authority.models import ExtendUser
import uuid
import paramiko
import socket
from deveops.utils.msg import Message
from deveops.utils import sshkey,aes
from utils.models import FILE
from django.contrib.auth.models import Group as PerGroup
from authority.models import Key,Jumper
from django.conf import settings

__all__ = [
]


class Monitor(models.Model):
    id = models.AutoField(primary_key=True)
    uuid = models.UUIDField(auto_created=True, default=uuid.uuid4, editable=False)
    class Meta:
        abstract = True
        permissions = (
            ('yo_monitor_aliyun', u'阿里云监控查看'),
            ('yo_monitor_vmware', u'VMware监控查看')
        )
