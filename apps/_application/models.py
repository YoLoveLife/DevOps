# -*- coding: utf-8 -*-
from manager.models import Host
from django.db import models
import uuid


# class ExpiredAliyunRDS(models.Model):
#     id = models.AutoField(primary_key=True)
#     uuid = models.UUIDField(auto_created=True, default=uuid.uuid4, editable=False)
#     status = models.CharField(max_length=100, default='')
#     dbinstanceid = models.CharField(max_length=100,default='')
#     expired = models.IntegerField(default='0')
#     dbinstancename = models.CharField(max_length=100,default='noname')
#     version = models.CharField(max_length=100,default='')
#     readonly = models.IntegerField(default='0')

# Create your models here.
#
# __all__=['BaseApplication','Redis','DB','DBDetail','DBUser']
#
# class BaseApplication(models.Model):
#     # id=models.AutoField(primary_key=True)
#     id = models.UUIDField(auto_created=True, default=uuid.uuid4, editable=False, primary_key=True)
#     host=models.ForeignKey(Host,default=None,blank=True,null=True)
#     version=models.CharField(max_length=10)
#     online=models.BooleanField(default=False)
#     class Meta:
#         abstract = True
#
# class Redis(BaseApplication):
#     redis_passwd = models.CharField(max_length=100,default='000000')
#     url = models.CharField(max_length=100,default='')
#     port = models.IntegerField(default='6379')
#     pidfile = models.CharField(max_length=100,default='/var/run/redis.pid')
#     logfile = models.CharField(max_length=100,default='/var/log/redis.log')
#     prefix=models.CharField(max_length=100,default='/usr/local/redis')
#
#     def get_access_url(self):
#         if self.host is None:
#             return self.redis_passwd+'@'+self.url
#         else:
#             return self.redis_passwd+'@'+self.host.connect_ip
#
#
# class DB(BaseApplication):
#     IS_SLAVE=(
#         (0,u'否'),
#         (1,u'是'),
#     )
#     url = models.CharField(max_length=100,default='')
#     root_passwd=models.CharField(max_length=100,default='')
#     port=models.IntegerField(default='3306')
#     socket=models.CharField(max_length=100,default='')
#     datadir=models.CharField(max_length=100,default='')
#     softlib=models.ForeignKey(Softlib,default=1,)
#     prefix=models.CharField(max_length=100,default='')
#     is_slave = models.IntegerField(default=0,choices=IS_SLAVE)
#
#     #集联更新
#     # def save(self):
#     #     return super(DB, self).save()
#
#     def get_all_user(self):
#         return self.dbuser.all()
#
# class DBDetail(models.Model):
#     # id = models.AutoField(primary_key=True)
#     id = models.UUIDField(auto_created=True, default=uuid.uuid4, editable=False, primary_key=True)
#     db = models.ForeignKey(DB,default=1,related_name='dbdetail')
#     com_insert = models.CharField(max_length=100,default=0)
#     com_update = models.CharField(max_length=100,default=0)
#     max_connections = models.CharField(max_length=100,default=0)
#     thread_running = models.CharField(max_length=100,default=0)
#
# class DBUser(models.Model):
#     # id = models.AutoField(primary_key=True)
#     id = models.UUIDField(auto_created=True, default=uuid.uuid4, editable=False, primary_key=True)
#     user = models.CharField(max_length=100,default='')
#     ip = models.CharField(max_length=16,default='')
#     db = models.ForeignKey(DB,default=1,related_name='dbuser')
#
#     def full_auth_name(self):
#         return self.user +'@'+ self.ip
#
#     def set_user(self,full_name):
#         list = full_name.split('@')
#         self.user = list[0]
#         self.ip = list[1]
#         self.save()
#
#     def get_access_url(self):
#         if self.db.host is None:#为空
#             return self.user+'@'+self.db.url+':'+self.db.port
#         else:
#             return self.user+'@'+self.db.host.connect_ip+':'+self.db.port


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
