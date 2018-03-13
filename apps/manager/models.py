# -*- coding:utf-8 -*-
from __future__ import unicode_literals
from django.utils.translation import ugettext_lazy as _
from django.db import models
from softlib.models import Softlib
from authority.models import ExtendUser
import uuid
from deveops.utils.msg import Message
from django.conf import settings
import paramiko
import socket
from deveops.utils import sshkey,aes
from django.core.exceptions import ValidationError

# Create your models here.
application_list= ['db_set','redis_set']#,'nginx_set']


class System_Type(models.Model):
    id = models.AutoField(primary_key=True) #全局ID
    name = models.CharField(max_length=50,default="") #字符长度

    def __unicode__(self):
        return self.name

    @property
    def sum_host(self):
        return self.hosts.count()

def private_key_validator(key):
    if not sshkey.private_key_validator(key):
        raise ValidationError(
            _('%(value)s is not an even number'),
            params={'value': key},
        )

class Sys_User(models.Model):
    BECOME_METHOD_CHOICES = (
        ('sudo', 'sudo'),
        ('su', 'su'),
    )
    id = models.IntegerField(primary_key=True)
    username = models.CharField(max_length=64)
    _password = models.CharField(max_length=256,blank=True,null=True)
    _private_key = models.TextField(max_length=4096,blank=True,null=True,validators=[private_key_validator])
    _public_key = models.TextField(max_length=4096,blank=True)
    become = models.BooleanField(default=True)
    become_method = models.CharField(choices=BECOME_METHOD_CHOICES,default='su',max_length=4)
    become_user = models.CharField(default='root',max_length=16)
    become_pass = models.CharField(default='',max_length=128)

    def __unicode__(self):
        return self.username

    __str__ = __unicode__

    @property
    def is_admin(self):
        if self.username == 'root':
            return True
        else:
            return False

    def groups_list(self):
        st = '|'
        if self.groups.size() >0:
            for group in self.groups:
                st.join(group.name)
        else:
            return ''
        return st

    @property
    def password(self):
        if self._password:
            return aes.decrypt(self._password)
        else:
            return ''

    @password.setter
    def password(self,passwd):
        self._password = aes.encrypt(passwd)

    @property
    def reco_private_key(self):
        return aes.decrypt(self._private_key)[0:7]

    @property
    def private_key(self):
        if self._private_key:
            key_str = aes.decrypt(self._private_key)
            return sshkey.ssh_private_key2obj(key_str)
        else:
            return None

    @private_key.setter
    def private_key(self,pri_key):
        self._private_key = aes.encrypt(pri_key)

    @property
    def public_key(self):
        return aes.decrypt(self._public_key)

    @public_key.setter
    def public_key(self, pub_key):
        self._public_key = aes.encrypt(pub_key)

def upload_dir_path(instance, filename):
    #instance.group.id,
    return u'framework/{0}'.format(filename)

class Group(models.Model):
    GROUP_STATUS=(
        (0,'禁用中'),
        (1,'使用中'),
        (2,'暂停中'),
    )
    id = models.AutoField(primary_key=True)
    uuid = models.UUIDField(default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100,default='')
    info = models.CharField(max_length=100,default='')
    framework = models.ImageField(upload_to=upload_dir_path,default='hacg.fun_01.jpg')
    users = models.ManyToManyField(ExtendUser,blank=True,related_name='users',verbose_name=_("users"))
    status = models.IntegerField(choices=GROUP_STATUS,default=0)
    sys_user = models.ManyToManyField(Sys_User,null=True,related_name='group')

    def __unicode__(self):
        return self.name

    __str__ = __unicode__

    def _name(self):
        return 'group'

    def users_list(self):
        st=","
        list=[]
        for user in self.users.all():
            list.append(user.get_full_name())
        if len(list) == 0:
            return ""
        else:
            return st.join(list)

    @property
    def catch_ssh_connect(self):
        if self.jumpers.count() <1:
            msg = Message()
            return msg.fuse_msg('该应用组无关联跳板机', None),0,0
        else:
            for jumper in self.jumpers.all():
                msg = jumper.catch_ssh_connect
                return msg, jumper.connect_ip, jumper.sshport


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
        strlist= []
        for r in result:
            strlist.append(r)
        return ",".join(strlist)

class HostDetail(models.Model):
    id=models.AutoField(primary_key=True) #全局ID
    coreness = models.CharField(max_length=5, default='')  # CPU数
    memory = models.CharField(max_length=7, default='')  # 内存
    root_disk = models.CharField(max_length=7, default="")  # 本地磁盘大小
    server_position = models.CharField(max_length=50,default='')#服务器位置
    systemtype = models.ForeignKey(System_Type,on_delete=models.SET_NULL,null=True,related_name='hosts')
    info = models.CharField(max_length=200,default="")

class Host(models.Model):
    SYSTEM_STATUS=(
        (0,'错误'),
        (1,'正常'),
        (2,'不可达'),
    )
    #主机标识
    id=models.AutoField(primary_key=True) #全局ID
    uuid = models.UUIDField(auto_created=True,default=uuid.uuid4,editable=False)

    #资产结构
    groups = models.ManyToManyField(Group,blank=True,related_name='hosts',verbose_name=_("Group"))#所属应用
    storages = models.ManyToManyField(Storage,blank=True,related_name='hosts',verbose_name=_('Host'))
    #相关信息
    connect_ip = models.GenericIPAddressField(default='',null=False)
    service_ip = models.GenericIPAddressField(default='0.0.0.0',null=True)

    hostname = models.CharField(max_length=50,default='localhost.localdomain')#主机名称
    sshport = models.IntegerField(default='52000')#用户端口
    detail = models.ForeignKey(HostDetail,related_name='host',on_delete=models.SET_NULL,null=True)
    status = models.IntegerField(default=1,choices=SYSTEM_STATUS)#服务器状态

    class Meta:
        permissions = (('yo_add_host', u'新增主机'),
                       ('yo_change_host',u'修改主机'),
                       ('yo_delete_host',u'删除主机'),
                       ('yo_passwd_host',u'获取主机密码'),
                       ('yo_webskt_host',u'远控主机'))

    def __unicode__(self):
        return self.hostname + ' - ' + self.connect_ip + ' - ' + self.info

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

    @property
    def catch_ssh_connect(self):
        target = paramiko.SSHClient()
        target.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        flag = 'host-none'
        msg = Message()
        for group in self.groups.all():
            msg,sship,sshport = group.catch_ssh_connect
            if msg.status == 1:
                try:
                    transport = msg.instance.get_transport()
                    dest_addr = (self.connect_ip,int(self.sshport))
                    local_addr = (sship,int(sshport))
                    jumperchannel = transport.open_channel("direct-tcpip", dest_addr, local_addr)
                    target.set_missing_host_key_policy(paramiko.AutoAddPolicy())

                    target.connect(self.connect_ip, username=self.sys_user.username,pkey=sshkey.ssh_private_key2obj(self.sys_user.private_key),
                                   sock=jumperchannel, port=int(self.sshport))
                    return msg.fuse_msg(1,u'主机连接成功',target)
                except paramiko.SSHException:
                    flag=u'主机SSH错误'
                    continue
                except socket.timeout:
                    flag=u'主机连接超时'
                    continue
                except socket.error:
                    flag=u'socket出错'
                    continue
                except Exception, ex:
                    flag=u'主机连接故障'
                    continue
            else:
                continue
        return msg.fuse_msg(0,flag,None)