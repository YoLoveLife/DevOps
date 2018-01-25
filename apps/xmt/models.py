# -*- coding:utf-8 -*-
from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import Group
from authority.models import ExtendUser
# Create your models here.
class XMT_Result(models.Model):
    id = models.AutoField(primary_key=True)
    result = models.TextField()
    class Meta:
        ordering = ['id']

class XMT(models.Model):
    APP_MODULE=(
        (0, u'未选择'),
        (1, u'op'),
        (2, u'act'),
        (3, u'auth'),
        (4, u'vote'),
        (5, u'api'),
        (6, u'uc'),
        (7, u'swoole'),
        (8, u'log'),
        (9,u'tool'),
    )
    DEPLOY_USER=(
        (0,u'未选择'),
        (1, u'于'),
        (2, u'余'),
        (3,u'张璐萍'),
        (4,u'巫上华'),
        (5,u'大佬黄'),
        (6,u'郑蕴华'),
        (7, u'老杨'),
        (8,u'陈晨'),
    )
    DEPLOY_ENV=(
        (0,u'未选择'),
        (1,u'pre'),
        (2,u'prod'),
    )
    DEPLOY_STATUS=(
        (0,u'执行中'),
        (1,u'执行完毕')
    )
    id = models.AutoField(primary_key=True)
    # name = models.IntegerField(default=0,choices=DEPLOY_USER)
    user = models.ForeignKey(ExtendUser,null=True)
    env = models.IntegerField(default=0,choices=DEPLOY_ENV)
    model = models.IntegerField(default=0,choices=APP_MODULE)
    gitlab = models.CharField(max_length=41,default='null')
    info = models.CharField(max_length=100,default='')
    time = models.DateTimeField(auto_now_add=True)#2000-01-01 00:00:00:00.000001
    status = models.IntegerField(choices=DEPLOY_STATUS,default=0)
    result = models.OneToOneField(XMT_Result,on_delete=models.CASCADE,null=True,related_name='mission')
    class Meta:
        ordering = ['-id']

    def __unicode__(self):
        return self.user.name

    def get_result(self):
        return '/xmt/result/'+str(self.result.id)+'/'

    __str__ = __unicode__