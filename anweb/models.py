# -*- coding:utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.
from django.db import models
class Soft(models.Model):
    id=models.IntegerField(primary_key=True)
    soft_name=models.CharField(max_length=100)

class Softlib(models.Model):
    id=models.IntegerField(primary_key=True)
    soft_type=models.ForeignKey(Soft)
    soft_version=models.CharField(max_length=10)
    soft_md5=models.CharField(max_length=100)

class State(models.Model):
    id=models.IntegerField(primary_key=True)
    state_name=models.CharField(max_length=100)

class Group(models.Model):
    id=models.AutoField(primary_key=True)
    group_name=models.CharField(max_length=100)
    remark=models.CharField(max_length=100)
    def toJSON(self):
        fields = []
        for field in self._meta.fields:
            fields.append(field.name)

        d = {}
        for attr in fields:
            d[attr] = getattr(self, attr)
        import json
        return json.dumps(d)

class Host(models.Model):
    id=models.IntegerField(primary_key=True)
    hostname=models.CharField(max_length=15,default='localhost')
    group_id=models.ForeignKey(Group)
    softlib_id=models.ForeignKey(Softlib,default=0)
    sship=models.CharField(max_length=15,default='192.168.1.1')
    sshpasswd=models.CharField(max_length=100,default='000000')
    sshport=models.CharField(max_length=5,default='22')
    state=models.IntegerField(default=0)

class Java(models.Model):
    id=models.IntegerField(primary_key=True)
    group_id=models.ForeignKey(Group)
    prefix=models.CharField(max_length=100,default='/usr/local')

class MySQL(models.Model):
    id=models.IntegerField(primary_key=True)
    group_id=models.ForeignKey(Group)
    prefix=models.CharField(max_length=100,default='/usr/local')
    mysqlpasswd=models.CharField(max_length=100,default='000000')
    port=models.IntegerField(default='3306')
    socket=models.CharField(max_length=100,default='/tmp/mysql.sock')
    datadir=models.CharField(max_length=100)
    key_buffer_size=models.CharField(max_length=100)
    table_open_cache=models.CharField(max_length=100)
    sort_buffer_size=models.CharField(max_length=100)
    read_buffer_size=models.CharField(max_length=100)
    read_rnd_buffer_size=models.CharField(max_length=100)
    query_cache_size=models.CharField(max_length=100)
    thread_cache_size=models.CharField(max_length=100)
    server_id=models.IntegerField()
    extend=models.CharField(max_length=100,default="")

class Nginx(models.Model):
    id=models.IntegerField(primary_key=True)
    group_id=models.ForeignKey(Group)
    prefix=models.CharField(max_length=100)
    workproc=models.CharField(max_length=100)
    pid=models.CharField(max_length=100)
    workconn=models.CharField(max_length=100)
    port=models.CharField(max_length=100,default='80')
    servername=models.CharField(max_length=100)
    locations=models.CharField(max_length=100,default='')

class Redis(models.Model):
    id=models.IntegerField(primary_key=True)
    group_id=models.ForeignKey(Group)
    prefix=models.CharField(max_length=100,default='/usr/local')
    bind=models.CharField(max_length=100,default='0.0.0.0')
    port=models.CharField(max_length=100,default='6379')
    appendonly=models.CharField(max_length=100)
    noonrewrite=models.CharField(max_length=100)
    saveoptions=models.CharField(max_length=100)
    datadir=models.CharField(max_length=100)
    requirepass=models.CharField(max_length=100)
    slaveof=models.CharField(max_length=100,default='')
    masterauth=models.CharField(max_length=100,default='')
    cluster_enabled=models.CharField(max_length=100,default='')
    cluster_config_file=models.CharField(max_length=100,default='')
    extend=models.CharField(max_length=100,default='')

class Tomcat(models.Model):
    id=models.IntegerField(primary_key=True)
    group_id=models.ForeignKey(Group)
    prefix=models.CharField(max_length=100,default='/usr/local')
    java_opts=models.CharField(max_length=100,default='')
