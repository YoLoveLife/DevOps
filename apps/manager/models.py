# -*- coding:utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.
from django.db import models
class Group(models.Model):
    id=models.AutoField(primary_key=True)
    name=models.CharField(max_length=100,default='None')
    info=models.CharField(max_length=100,default='None')

class Storage(models.Model):
    id=models.AutoField(primary_key=True)#全局ID
    disk_size=models.CharField(max_length=100,default="0G")
    disk_path=models.CharField(max_length=100,default="//10.100.100.246/storage")
    info=models.CharField(max_length=100,default="NoUse")

class Host(models.Model):
    id=models.AutoField(primary_key=True) #全局ID
    group = models.ForeignKey(Group,default=1,related_name='host_set')#所属应用
    storages = models.ManyToManyField(Storage,related_name='storage_set')
    systemtype=models.CharField(max_length=50,default='centos6.5')#操作系统
    manage_ip = models.CharField(max_length=15, default='10.100.100.246')#管理IP
    service_ip = models.CharField(max_length=15, default='10.100.100.246')#服务IP
    outer_ip = models.CharField(max_length=15, default='10.100.100.246')#外网IP
    server_position = models.CharField(max_length=50,default='Vmware')#服务器位置
    hostname = models.CharField(max_length=50,default='localhost')#主机名称
    normal_user = models.CharField(max_length=15, default='QbDev')#普通用户
    sshpasswd = models.CharField(max_length=100,default='000000')#用户密码
    sshport = models.CharField(max_length=5,default='52000')#用户端口
    coreness = models.IntegerField(default=2)#CPU数
    memory = models.IntegerField(default=2048)#内存
    root_disk=models.IntegerField(default=20)#本地磁盘大小
    share_disk_path=models.CharField(max_length=200)#共享路径
    share_disk=models.IntegerField(default=30)#共享磁盘大小
    info=models.CharField(max_length=200,default="无信息")