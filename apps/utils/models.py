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
    'FILE', 'IMAGE'
]


def upload_image_path(instance,filename):
    t = filename.split('.')
    return 'framework' + '/' + str(instance.uuid)


def upload_file_path(instance,filename):
    t = filename.split('.')
    return 'work/' + str(instance.uuid)


class FILE(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(default=uuid.uuid4, max_length=100, null=True, blank=True)
    # 文件使用时注入的参数名称
    var_name = models.CharField(default='', max_length=100 ,null=True, blank=True)
    uuid = models.UUIDField(auto_created=True, default=uuid.uuid4, editable=False)
    file = models.FileField(upload_to=upload_file_path, null=True, blank=True)
    # 上传时间
    create_time = models.DateTimeField(auto_now_add=True)
    # 上传用户
    user = models.ForeignKey(ExtendUser, default=None, blank=True, null=True, on_delete=models.SET_NULL)

    class Meta:
        permissions = (
            ('yo_list_file', u'罗列文件'),
            ('yo_create_file', u'上传文件'),
            ('yo_delete_file', u'删除文件'),
        )

    @property
    def mission_used(self):
        if self.pushmission is None:
            return '未使用'
        else:
            return self.pushmission.get().works.get().uuid


class IMAGE(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(default=uuid.uuid4, max_length=100, null=True, blank=True)
    uuid = models.UUIDField(auto_created=True, default=uuid.uuid4, editable=False)
    image = models.ImageField(upload_to=upload_image_path, null=True, blank=True)
    # 上传时间
    create_time = models.DateTimeField(auto_now_add=True)
    # 上传用户
    user = models.ForeignKey(ExtendUser, default=None, blank=True, null=True, on_delete=models.SET_NULL)

    class Meta:
        permissions = (
            ('yo_list_image', u'罗列图片'),
            ('yo_create_image', u'上传图片'),
            ('yo_delete_image', u'删除图片'),
        )
