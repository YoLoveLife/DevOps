from __future__ import unicode_literals

from django.db import models

# Create your models here.
from django.db import models
class Soft(models.Model):
    id=models.IntegerField(primary_key=True)
    soft_name=models.CharField(max_length=100)
class Softlib(models.Model):
    id=models.IntegerField(primary_key=True,max_length=10)
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
    port=models.IntegerField(max_length=10)
    socket=models.CharField(max_length=100)
    datadir=models.CharField(max_length=100)
    key_buffer_size=models.CharField(max_length=100)
    table_open_cache=models.CharField(max_length=100)
    sort_buffer_size=models.CharField(max_length=100)
    read_buffer_size=models.CharField(max_length=100)
    read_rnd_buffer_size=models.CharField(max_length=100)
    query_cache_size=models.CharField(max_length=100)
    thread_cache_size=models.CharField(max_length=100)
    server_id=models.IntegerField(max_length=10)
    extend=models.CharField(max_length=100)
'''
port='3306',socket='/tmp/mysql.sock',prefix='/usr/local',datadir='/usr/local/mysql/data',
                            key_buffer_size='256M',table_open_cache='256',sort_buffer_size='1M',read_buffer_size='1M',read_rnd_buffer_size='4M',
                            query_cache_size='16M',thread_cache_size='8',server_id='1',extend=''
'''