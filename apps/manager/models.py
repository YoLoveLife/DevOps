# -*- coding:utf-8 -*-
from __future__ import unicode_literals
from django.utils.translation import ugettext_lazy as _
from django.db import models
from softlib.models import Softlib
# Create your models here.
list= ['db_set']#,'redis_set','nginx_set']
class Group(models.Model):
    id=models.AutoField(primary_key=True)
    name=models.CharField(max_length=100,default='')
    info=models.CharField(max_length=100,default='')

class Storage(models.Model):
    id=models.AutoField(primary_key=True)#全局ID
    disk_size=models.CharField(max_length=100,default="")
    disk_path=models.CharField(max_length=100,default="")
    info=models.CharField(max_length=100,default="")

    def get_all_group_name(self):
        list = []
        for host in self.hosts.all():
            for group in host.groups.all():
                list.append(group.name)
        result={}.fromkeys(list).keys()
        str = ""
        for r in result:
            str = str + r +','
        return str[0:-1]

class Host(models.Model):
    SYSTEM_CHOICES=(
        (0,u'未添加'),
        (1,u'Windows Server 2006'),
        (2,u'Windows Server 2008'),
        (3,u'Centos 6.5'),
        (4,u'Centos 7.1'),
    )
    SYSTEM_STATUS=(
        (0,'错误'),
        (1,'正常'),
        (2,'不可达'),
    )
    id=models.AutoField(primary_key=True) #全局ID
    groups = models.ManyToManyField(Group,blank=True,related_name='hosts',verbose_name=_("Group"))#所属应用
    storages = models.ManyToManyField(Storage,blank=True,related_name='hosts',verbose_name=_('Host'))
    systemtype=models.IntegerField(default=0,choices=SYSTEM_CHOICES)#操作系统
    manage_ip = models.CharField(max_length=15, default='')#管理IP
    service_ip = models.CharField(max_length=15, default='')#服务IP
    outer_ip = models.CharField(max_length=15, default='')#外网IP
    server_position = models.CharField(max_length=50,default='')#服务器位置
    hostname = models.CharField(max_length=50,default='localhost.localdomain')#主机名称
    normal_user = models.CharField(max_length=15, default='')#普通用户
    sshpasswd = models.CharField(max_length=100,default='')#用户密码
    sshport = models.CharField(max_length=5,default='')#用户端口
    coreness = models.CharField(max_length=5,default='')#CPU数
    memory = models.CharField(max_length=7,default='')#内存
    root_disk = models.CharField(max_length=7,default="")#本地磁盘大小
    info = models.CharField(max_length=200,default="")
    status = models.IntegerField(default=1,choices=SYSTEM_STATUS)#服务器状态

    def application_get(self):
        id_list=[]
        for attr in list:
            if getattr(self,attr).count() == 0:
                pass
            else:
                id_list.append(int(getattr(self,attr).get().softlib_id))
        if Softlib.objects.filter(id__in=id_list).count() == 0:
            softlibs = []
        else:
            softlibs = Softlib.objects.filter(id__in=id_list)
        return softlibs
