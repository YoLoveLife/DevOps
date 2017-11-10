# -*- coding: utf-8 -*-
from __future__ import unicode_literals
# from softlib.models import Softlib
from manager.models import Host
from softlib.models import Softlib
from django.db import models
# Create your models here.
#
__all__=['DB','DBDetail','DBUser']

class DB(models.Model):
    IS_SLAVE=(
        (0,u'否'),
        (1,u'是'),
    )
    id=models.AutoField(primary_key=True)
    host=models.ForeignKey(Host,default=1)
    prefix=models.CharField(max_length=100,default='/usr/local/mysql')
    root_passwd=models.CharField(max_length=100,default='000000')
    port=models.IntegerField(default='3306')
    socket=models.CharField(max_length=100,default='/tmp/mysql.sock')
    datadir=models.CharField(max_length=100,default='/storage/mysql')
    softlib=models.ForeignKey(Softlib,default=1,)
    is_slave = models.IntegerField(default=0,choices=IS_SLAVE)
    online=models.BooleanField(default=False)

    def get_all_user(self):
        return self.dbuser.all()


class DBDetail(models.Model):
    id = models.AutoField(primary_key=True)
    db = models.ForeignKey(DB,default=1,related_name='dbdetail')
    com_insert = models.CharField(max_length=100,default=0)
    com_update = models.CharField(max_length=100,default=0)
    max_connections = models.CharField(max_length=100,default=0)
    thread_running = models.CharField(max_length=100,default=0)

class DBUser(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.CharField(max_length=100,default='')
    ip = models.CharField(max_length=16,default='')
    db = models.ForeignKey(DB,default=1,related_name='dbuser')

    def full_auth_name(self):
        return self.user +'@'+ self.ip

    def set_user(self,full_name):
        list = full_name.split('@')
        self.user = list[0]
        self.ip = list[1]
        self.save()

#
#
# class Java(models.Model):
#     id=models.AutoField(primary_key=True)
#     host=models.ForeignKey(Host,default=1)
#     prefix=models.CharField(max_length=100,default='/usr/local')
#     softlib=models.ForeignKey(Softlib,default=1)
#
# class Tomcat(models.Model):
#     id=models.AutoField(primary_key=True)
#     host=models.ForeignKey(Host,default=None)
#     prefix=models.CharField(max_length=100,default='')
#     port=models.CharField(max_length=6,default='')
#     web_xml=models.CharField(max_length=100,default='')
#     java_opts=models.CharField(max_length=100,default='')
#     log=models.CharField(max_length=100,default='')
#     softlib=models.ForeignKey(Softlib,default=1)
#
#
# class Nginx(models.Model):
#     id=models.AutoField(primary_key=True)
#     host=models.ForeignKey(Host,default=1)
#     prefix=models.CharField(max_length=100,default='/usr/local')
#     pid=models.CharField(max_length=100)
#     port=models.CharField(max_length=100,default='80')
#     softlib=models.ForeignKey(Softlib,default=1)
#     online=models.BooleanField(default=False)
#
# class Redis(models.Model):
#     id=models.AutoField(primary_key=True)
#     host=models.ForeignKey(Host,default=1)
#     prefix=models.CharField(max_length=100,default='/usr/local')
#     bind=models.CharField(max_length=100,default='0.0.0.0')
#     port=models.CharField(max_length=100,default='6379')
#     datadir=models.CharField(max_length=100)
#     requirepass=models.CharField(max_length=100)
#     softlib=models.ForeignKey(Softlib,default=1)
#     online=models.BooleanField(default=False)
