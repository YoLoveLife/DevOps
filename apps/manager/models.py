# -*- coding:utf-8 -*-
from __future__ import unicode_literals
from django.utils.translation import ugettext_lazy as _
from django.db import models
from softlib.models import Softlib
from authority.models import ExtendUser
from deveops.utils import aes
# Create your models here.
application_list= ['db_set','redis_set']#,'nginx_set']

def upload_dir_path(instance, filename):
    #instance.group.id,
    return u'framework/{0}'.format(filename)

class System_Type(models.Model):
    id = models.AutoField(primary_key=True) #全局ID
    name = models.CharField(max_length=50,default="") #字符长度

    def __unicode__(self):
        return self.name

class Group(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100,default='')
    info = models.CharField(max_length=100,default='')
    framework = models.ImageField(upload_to=upload_dir_path,default='hacg.fun_01.jpg')
    users = models.ManyToManyField(ExtendUser,blank=True,related_name='users',verbose_name=_("users"))

    def __unicode__(self):
        return self.name

    __str__ = __unicode__

    def _name(self):
        return 'group'

class Storage(models.Model):
    id=models.AutoField(primary_key=True)#全局ID
    disk_size=models.CharField(max_length=100,default="")
    disk_path=models.CharField(max_length=100,default="")
    info=models.CharField(max_length=100,default="")

    def __unicode__(self):
        return self.disk_path + ' - ' + self.info

    __str__ = __unicode__

    def _name(self):
        return 'storage'

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
    SYSTEM_STATUS=(
        (0,'错误'),
        (1,'正常'),
        (2,'不可达'),
    )
    id=models.AutoField(primary_key=True) #全局ID
    groups = models.ManyToManyField(Group,blank=True,related_name='hosts',verbose_name=_("Group"))#所属应用
    storages = models.ManyToManyField(Storage,blank=True,related_name='hosts',verbose_name=_('Host'))
    systemtype = models.ForeignKey(System_Type,on_delete=models.SET_NULL,null=True)

    manage_ip = models.GenericIPAddressField(default='0.0.0.0')
    service_ip = models.GenericIPAddressField(default='0.0.0.0')
    outer_ip = models.GenericIPAddressField(default='0.0.0.0')
    server_position = models.CharField(max_length=50,default='')#服务器位置
    hostname = models.CharField(max_length=50,default='localhost.localdomain')#主机名称
    normal_user = models.CharField(max_length=15, default='')#普通用户
    sshpasswd = models.CharField(max_length=100,default='')#用户密码
    sshport = models.IntegerField(default='52000')#用户端口
    coreness = models.CharField(max_length=5,default='')#CPU数
    memory = models.CharField(max_length=7,default='')#内存
    root_disk = models.CharField(max_length=7,default="")#本地磁盘大小
    info = models.CharField(max_length=200,default="")
    status = models.IntegerField(default=1,choices=SYSTEM_STATUS)#服务器状态

    def __unicode__(self):
        return self.hostname + ' - ' + self.service_ip + ' - ' + self.info

    __str__ = __unicode__

    def _name(self):
        return 'host'

    def password_get(self):
        return aes.decrypt(self.sshpasswd)

    def application_get(self): ####Application Link to Host
        id_list=[]
        for attr in application_list:
            if getattr(self,attr).count() == 0:
                pass
            else:
                if getattr(self,attr).count() == 1:
                    id_list.append(int(getattr(self,attr).get().softlib_id))
                else:
                    for mols in getattr(self,attr).all():
                        id_list.append(int(mols.softlib_id))
        if Softlib.objects.filter(id__in=id_list).count() == 0:
            softlibs = []
        else:
            softlibs = Softlib.objects.filter(id__in=id_list)
        return softlibs

    def manage_user_get(self):
        dist = {}
        for group in self.groups.all():
            for user in group.users.all():
                dist[user.email]=user
        list = []
        for key in dist:
            list.append(dist[key])
        return list