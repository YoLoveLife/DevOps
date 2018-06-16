# -*- coding:utf-8 -*-
from django.utils.translation import ugettext_lazy as _
from django.db import models
import uuid
__all__ = [
    "ExpiredAliyun",
    "ExpiredAliyunECS",
    "ExpiredAliyunRDS",
]


class ExpiredAliyun(models.Model):
    id = models.AutoField(primary_key=True)
    uuid = models.UUIDField(auto_created=True, default=uuid.uuid4, editable=False)
    status = models.CharField(max_length=100, default='')
    expired = models.IntegerField(default='0')

    class Meta:
        ordering = ['expired', 'id']
        abstract = True


class ExpiredAliyunECS(ExpiredAliyun):
    connect_ip = models.GenericIPAddressField(default='', null=True)
    tags = models.CharField(max_length=100,default='')
    recognition_id = models.CharField(max_length=100,default='')
    instancename = models.CharField(max_length=100,default='noname')


class ExpiredAliyunRDS(ExpiredAliyun):
    recognition_id = models.CharField(max_length=100,default='')
    instancename = models.CharField(max_length=100,default='noname')
    version = models.CharField(max_length=100,default='')
    readonly = models.IntegerField(default='0')


class ExpiredAliyunKVStore(ExpiredAliyun):
    recognition_id = models.CharField(max_length=100,default='')
    instancename = models.CharField(max_length=100, default='noname')
    connect_domain = models.CharField(max_length=100,default='0.0.0.0')
    version = models.CharField(max_length=100, default='4.0')
    type = models.CharField(max_length=100, default='redis')


class ExpiredAliyunMongoDB(ExpiredAliyun):
    recognition_id = models.CharField(max_length=100,default='')
    instancename = models.CharField(max_length=100, default='noname')
    version = models.CharField(max_length=100, default='4.0')
    type = models.CharField(max_length=100, default='MongoDB')
