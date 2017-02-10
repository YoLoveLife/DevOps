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

class Group(models.Model):
    id=models.IntegerField(primary_key=True)
    group_name=models.CharField(max_length=100)
    remark=models.CharField(max_length=100)

class Host(models.Model):
    id=models.IntegerField(primary_key=True)
    group_id=models.ForeignKey(Group)
    softlib_id=models.ForeignKey(Softlib)

class Java(models.Model):
    id=models.IntegerField(primary_key=True)
    group_id=models.ForeignKey(Group)
    prefix=models.CharField(max_length=100)

class MySQL(models.Model):
    id=models.IntegerField(primary_key=True)
    group_id=models.ForeignKey(Group)
    prefix=models.CharField(max_length=100)
    mysqlpasswd=models.CharField(max_length=100)
    port=models.IntegerField()
    socket=models.CharField(max_length=100)
    datadir=models.CharField(max_length=100)
    key_buffer_size=models.CharField(max_length=100)
    table_open_cache=models.CharField(max_length=100)
    sort_buffer_size=models.CharField(max_length=100)
    read_buffer_size=models.CharField(max_length=100)
    read_rnd_buffer_size=models.CharField(max_length=100)
    query_cache_size=models.CharField(max_length=100)
    thread_cache_size=models.CharField(max_length=100)
    server_id=models.IntegerField()
    extend=models.CharField(max_length=100)

class Nginx(models.Model):
    id=models.IntegerField(primary_key=True)
    group_id=models.ForeignKey(Group)
    prefix=models.CharField(max_length=100)
    workproc=models.CharField(max_length=100)
    pid=models.CharField(max_length=100)
    workconn=models.CharField(max_length=100)
    port=models.CharField(max_length=100)
    servername=models.CharField(max_length=100)
    locations=models.CharField(max_length=100)

class Redis(models.Model):
    id=models.IntegerField(primary_key=True)
    group_id=models.ForeignKey(Group)
    prefix=models.CharField(max_length=100)
    bind=models.CharField(max_length=100)
    port=models.CharField(max_length=100)
    appendonly=models.CharField(max_length=100)
    noonrewrite=models.CharField(max_length=100)
    saveoptions=models.CharField(max_length=100)
    datadir=models.CharField(max_length=100)
    requirepass=models.CharField(max_length=100)
    slaveof=models.CharField(max_length=100)
    masterauth=models.CharField(max_length=100)
    cluster_enabled=models.CharField(max_length=100)
    cluster_config_file=models.CharField(max_length=100)
    extend=models.CharField(max_length=100)

class Tomcat(models.Model):
    id=models.IntegerField(primary_key=True)
    group_id=models.ForeignKey(Group)
    prefix=models.CharField(max_length=100)
    java_opts=models.CharField(max_length=100)
