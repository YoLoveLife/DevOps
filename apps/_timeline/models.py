# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.utils.translation import ugettext_lazy as _
from django.db import models
from django.contrib.auth.models import User
from authority.models import ExtendUser
from manager.models import Host
# from concert.models import Music
from execute.models import Callback
import uuid
# Create your models here.
STATUS = (
    (0, u'正在运行'),
    (1, u'运行成功'),
    (2, u'运行失败'),
)
HISTORY_TYPE = (
    (0, u'资产管理'),
    (1, u'脚本修改'),
    (2, u'剧本修改'),
    (3, u'人员管理'),
    (4, u'应用管理'),
    (5, u'密码获取'),
)
class History(models.Model):
    # id = models.AutoField(primary_key=True)
    id = models.UUIDField(auto_created=True, default=uuid.uuid4, editable=False, primary_key=True)
    hosts = models.ManyToManyField(Host,blank=True,related_name='hosts',verbose_name=_("Host"))
    user = models.ForeignKey(ExtendUser, default=1, related_name='startuser') #发起用户
    type = models.IntegerField(default=0,choices=HISTORY_TYPE)#历史类型
    info = models.TextField(default='')#信息
    status = models.IntegerField(default=0,choices=STATUS)#状态
    starttime = models.DateTimeField(auto_now_add=True,blank=True)#历史开始时间
    endtime = models.DateTimeField(auto_now=True,blank=True)#历史结束时间

class ConcertHistory(models.Model):
    id = models.UUIDField(auto_created=True, default=uuid.uuid4, editable=False, primary_key=True)
    # id = models.AutoField(primary_key=True)
    plantime = models.DateTimeField(auto_now=True,blank=True)#计划时间
    starttime = models.DateTimeField(auto_now_add=True,blank=True)#历史开始时间
    endtime = models.DateTimeField(auto_now=True,blank=True)#历史结束时间
    info = models.TextField(default='')#信息
    status = models.IntegerField(default=0,choices=STATUS)#状态
    # music = models.ForeignKey(Music,default=1,related_name='concert_his')#使用的音乐
    callback = models.ForeignKey(Callback,default=1,related_name='concert_back')#执行日志
    #
    # def get_last_history(self):
    #     self.objects.filter(plantime__day= )