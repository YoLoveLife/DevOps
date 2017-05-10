# -*- coding:utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.
from django.db import models
class Soft(models.Model):
    id=models.AutoField(primary_key=True)
    soft_name=models.CharField(max_length=100)

class Softlib(models.Model):
    id=models.AutoField(primary_key=True)
    soft_type=models.ForeignKey(Soft)
    soft_version=models.CharField(max_length=10)
    soft_md5=models.CharField(max_length=100)

class State(models.Model):
    id=models.AutoField(primary_key=True)
    state_name=models.CharField(max_length=100)

class Group(models.Model):
    id=models.AutoField(primary_key=True)
    name=models.CharField(max_length=100)
    remark=models.CharField(max_length=100)

class Host(models.Model):
    id=models.AutoField(primary_key=True)
    name=models.CharField(max_length=50,default='localhost')
    group=models.ForeignKey(Group,default=1)
    sship=models.CharField(max_length=15,default='192.168.1.1')
    sshpasswd=models.CharField(max_length=100,default='000000')
    sshport=models.CharField(max_length=5,default='22')

class Java(models.Model):
    id=models.AutoField(primary_key=True)
    host=models.ForeignKey(Host,default=1)
    prefix=models.CharField(max_length=100,default='/usr/local')
    softlib=models.ForeignKey(Softlib,default=1)

class MySQL(models.Model):
    id=models.AutoField(primary_key=True)
    host=models.ForeignKey(Host,default=1)
    prefix=models.CharField(max_length=100,default='/usr/local')
    passwd=models.CharField(max_length=100,default='000000')
    port=models.IntegerField(default='3306')
    socket=models.CharField(max_length=100,default='/tmp/mysql.sock')
    datadir=models.CharField(max_length=100,default='/storage/mysql')
    softlib=models.ForeignKey(Softlib,default=1)

class Nginx(models.Model):
    id=models.AutoField(primary_key=True)
    host=models.ForeignKey(Host,default=1)
    prefix=models.CharField(max_length=100,default='/usr/local')
    pid=models.CharField(max_length=100)
    port=models.CharField(max_length=100,default='80')
    softlib=models.ForeignKey(Softlib,default=1)

class Redis(models.Model):
    id=models.AutoField(primary_key=True)
    host=models.ForeignKey(Host,default=1)
    prefix=models.CharField(max_length=100,default='/usr/local')
    bind=models.CharField(max_length=100,default='0.0.0.0')
    port=models.CharField(max_length=100,default='6379')
    datadir=models.CharField(max_length=100)
    requirepass=models.CharField(max_length=100)
    softlib=models.ForeignKey(Softlib,default=1)

class Tomcat(models.Model):
    id=models.AutoField(primary_key=True)
    host=models.ForeignKey(Host,default=1)
    prefix=models.CharField(max_length=100,default='/usr/local')
    java_opts=models.CharField(max_length=100,default='')
    softlib=models.ForeignKey(Softlib,default=1)

class Operation(models.Model):
    id=models.AutoField(primary_key=True)
    oper_name=models.CharField(max_length=100,default=0)

class History(models.Model):
    id=models.AutoField(primary_key=True)#操作ID
    oper_type=models.ForeignKey(Operation)#操作类型
    oper_time=models.DateField()#操作时间
    oper_group=models.ForeignKey(Group)#操作组
    oper_info=models.CharField(max_length=100)#操作信息



