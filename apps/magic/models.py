# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from softlib.models import Softlib
from manager.models import Host
from django.db import models
# Create your models here.

class Java(models.Model):
    id=models.AutoField(primary_key=True)
    host=models.ForeignKey(Host,default=1)
    prefix=models.CharField(max_length=100,default='/usr/local')
    softlib=models.ForeignKey(Softlib,default=1)

class Tomcat(models.Model):
    id=models.AutoField(primary_key=True)
    host=models.ForeignKey(Host,default=None)
    prefix=models.CharField(max_length=100,default='')
    port=models.CharField(max_length=6,default='')
    web_xml=models.CharField(max_length=100,default='')
    java_opts=models.CharField(max_length=100,default='')
    log=models.CharField(max_length=100,default='')
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
    online=models.BooleanField(default=False)

class Nginx(models.Model):
    id=models.AutoField(primary_key=True)
    host=models.ForeignKey(Host,default=1)
    prefix=models.CharField(max_length=100,default='/usr/local')
    pid=models.CharField(max_length=100)
    port=models.CharField(max_length=100,default='80')
    softlib=models.ForeignKey(Softlib,default=1)
    online=models.BooleanField(default=False)

class Redis(models.Model):
    id=models.AutoField(primary_key=True)
    host=models.ForeignKey(Host,default=1)
    prefix=models.CharField(max_length=100,default='/usr/local')
    bind=models.CharField(max_length=100,default='0.0.0.0')
    port=models.CharField(max_length=100,default='6379')
    datadir=models.CharField(max_length=100)
    requirepass=models.CharField(max_length=100)
    softlib=models.ForeignKey(Softlib,default=1)
    online=models.BooleanField(default=False)
