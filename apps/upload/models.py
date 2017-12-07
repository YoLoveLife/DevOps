# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
from manager.models import Group,Storage
from django.conf import settings
# Create your models here.

def upload_dir_path(instance, filename):
    return u'group_{0}/{1}'.format(instance.group.id, filename)

def upload_group_dir(instance, filename):
    return u'group_{0}/{1}'.format(instance.group.id, filename)

def upload_storage_dir(instance, filename):
    return u'storage/{0}'.format(filename)

class Upload(object):
    def get_full_path(self):
        return settings.MEDIA_ROOT+'/%s'%(self.file)

class GroupUpload(Upload,models.Model):
    STATUS_CHOICES=(
        (0,u'未解析'),
        (1,u'解析完毕'),
    )
    id=models.AutoField(primary_key=True)
    file = models.FileField(upload_to=upload_group_dir,default='')
    group = models.ForeignKey(Group,default=1)
    status = models.IntegerField(default=0,choices=STATUS_CHOICES)


class StorageUpload(Upload,models.Model):
    STATUS_CHOICES=(
        (0,u'未解析'),
        (1,u'解析完毕'),
    )
    id=models.AutoField(primary_key=True)
    file = models.FileField(upload_to=upload_storage_dir,default='user_default/default.xls')
    status = models.IntegerField(default=0,choices=STATUS_CHOICES)
