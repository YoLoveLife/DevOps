# -*- coding: utf-8 -*-
# !/usr/bin/env python
# Time 18-1-18
# Author Yo
# Email YoLoveLife@outlook.com
from __future__ import unicode_literals
from django.db import models
from django.conf import settings
from authority.models import ExtendUser
import uuid
__all__ = [
    'FILE',
]


def upload_media_path(instance,filename):
    t = filename.split('.')
    return settings.MEDIA_ROOT + str(instance.uuid)+'.'+t[-1]


def upload_file_path(instance,filename):
    t = filename.split('.')
    return settings.OPS_DIR + str(instance.uuid) + '.' + t[-1]


class FILE(models.Model):
    id = models.AutoField(primary_key=True)
    uuid = models.UUIDField(auto_created=True, default=uuid.uuid4, editable=False)
    file = models.FileField(upload_to=upload_media_path,)
    # 上传时间
    create_time = models.DateTimeField(auto_now_add=True)
    # 上传用户
    user = models.ForeignKey(ExtendUser, default=None, blank=True, null=True)

    class Meta:
        permissions = (
            ('yo_list_file', u'罗列文件'),
            ('yo_create_file', u'上传文件'),
            ('yo_delete_file', u'删除文件'),
        )

class IMAGE(models.Model):
    id = models.AutoField(primary_key=True)
    uuid = models.UUIDField(auto_created=True, default=uuid.uuid4, editable=False)
    file = models.FileField(upload_to=upload_media_path,)
    # 上传时间
    create_time = models.DateTimeField(auto_now_add=True)
    # 上传用户
    user = models.ForeignKey(ExtendUser, default=None, blank=True, null=True)

    class Meta:
        permissions = (
            ('yo_list_image', u'罗列图像'),
            ('yo_create_image', u'上传图像'),
            ('yo_delete_image', u'删除图像'),
        )