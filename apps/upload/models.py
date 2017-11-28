# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
from manager.models import Group
from django.conf import settings
# Create your models here.

def upload_dir_path(instance,filename):
    return u'group_{0}/{1}'.format(instance.group.id,filename)

class GroupUpload(models.Model):
    STATUS_CHOICES=(
        (0,u'未解析'),
        (1,u'解析完毕'),
    )
    id=models.AutoField(primary_key=True)
    file = models.FileField(upload_to=upload_dir_path,default='user_default/default.xls')
    group = models.ForeignKey(Group,default=1)
    status = models.IntegerField(default=0)

    def get_full_path(self):
        return settings.MEDIA_ROOT+'/group_%s/%s'%(self.group_id,self.file)
