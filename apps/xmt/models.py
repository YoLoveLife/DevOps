# -*- coding:utf-8 -*-
from __future__ import unicode_literals
from django.db import models
# Create your models here.

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
    id = models.AutoField(primary_key=True)
    name = models.IntegerField(default=0,choices=DEPLOY_USER)
    env = models.IntegerField(default=0,choices=DEPLOY_ENV)
    model = models.IntegerField(default=0,choices=APP_MODULE)
    gitlab = models.CharField(max_length=41,default='null')

    def __unicode__(self):
        return self.name

    __str__ = __unicode__

class XMT_Result(models.Model):
    id = models.AutoField(primary_key=True)
    result = models.TextField()