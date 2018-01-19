# -*- coding:utf-8 -*-
from __future__ import unicode_literals
from django.db import models
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
    )
    DEPLOY_USER=(
        (0,u'未选择'),
        (1,u'张璐萍'),
        (2,u'老杨'),
        (3,u'巫上华'),
        (4,u'大佬黄'),
        (5,u'郑蕴华'),
        (6,u'陈晨'),
        (7, u'于'),
        (8, u'余'),
    )
    DEPLOY_ENV=(
        (0,u'未选择'),
        (1,u'pre'),
    )
    DEPLOY_STATUS=(
        (0,u'执行中'),
        (1,u'执行完毕')
    )
    id = models.AutoField(primary_key=True)
    name = models.IntegerField(default=0,choices=DEPLOY_USER)
    env = models.IntegerField(default=0,choices=DEPLOY_ENV)
    model = models.IntegerField(default=0,choices=APP_MODULE)
    gitlab = models.CharField(max_length=41,default='null')
    time = models.DateTimeField(auto_now_add=True)#2000-01-01 00:00:00:00.000001
    status = models.IntegerField(choices=DEPLOY_STATUS,default=0)
    result = models.OneToOneField(XMT_Result,on_delete=models.CASCADE,null=True,related_name='mission')
    class Meta:
        ordering = ['-id']

    def __unicode__(self):
        return self.name

    def get_result(self):
        return '/xmt/result/'+str(self.result.id)+'/'

    __str__ = __unicode__