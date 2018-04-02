# -*- coding:utf-8 -*-
from __future__ import unicode_literals
from django.utils.translation import ugettext_lazy as _
from django.db import models
from authority.models import ExtendUser
import uuid
import paramiko
import socket
from deveops.utils.msg import Message
from deveops.utils import sshkey,aes
from django.contrib.auth.models import Group as PerGroup
from authority.models import Key,Jumper

__all__ = [
    "System_Type", "Group", "Host",
    "Storage", "Position", "HostDetail"
]


class System_Type(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50, default="")

    class Meta:
        permissions = (('yo_list_systype', u'罗列系统类型'),
                       ('yo_create_systype', u'新增系统类型'),
                       ('yo_update_systype', u'修改系统类型'),
                       ('yo_detail_systype', u'详细系统类型'),
                       ('yo_delete_systype', u'删除系统类型'))

    def __unicode__(self):
        return self.name

    @property
    def sum_host(self):
        return self.hosts.count()


class Position(models.Model):
    id = models.AutoField(primary_key=True) #全局ID
    name = models.CharField(max_length=50, default="") #字符长度

    class Meta:
        permissions = (('yo_list_position', u'罗列位置'),
                       ('yo_create_position', u'新增位置'),
                       ('yo_update_position', u'修改位置'),
                       ('yo_detail_position', u'详细位置'),
                       ('yo_delete_position', u'删除位置'))

    def __unicode__(self):
        return self.name


def upload_dir_path(filename):
    # instance.group.id,
    return u'framework/{0}'.format(filename)


class Group(models.Model):
    GROUP_STATUS=(
        (0, '禁用中'),
        (1, '使用中'),
        (2, '暂停中'),
        (3, '不可达'),
    )
    id = models.AutoField(primary_key=True)
    uuid = models.UUIDField(auto_created=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100, default='')
    info = models.CharField(max_length=100, default='')
    framework = models.ImageField(upload_to=upload_dir_path, default='hacg.fun_01.jpg')
    users = models.ManyToManyField(ExtendUser, blank=True, related_name='assetgroups', verbose_name=_("assetgroups"))
    _status = models.IntegerField(choices=GROUP_STATUS, default=0)
    pmn_groups = models.ManyToManyField(PerGroup, blank=True, related_name='assetgroups', verbose_name=_("assetgroups"))

    # 操作凭证
    key = models.OneToOneField(Key, related_name='group', on_delete=models.SET_NULL, null=True, blank=True)
    jumper = models.OneToOneField(Jumper, related_name='group', on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        permissions = (('yo_list_group', u'罗列应用组'),
                       ('yo_create_group', u'新增应用组'),
                       ('yo_update_group', u'修改应用组'),
                       ('yo_detail_group', u'详细查看应用组'),
                       ('yo_delete_group', u'删除应用组'))

    def __unicode__(self):
        return self.name

    __str__ = __unicode__

    @property
    def status(self):
        return self._status

    @status.setter
    def status(self, status):
        if status == 1:
            if self.key is not None and self.jumper is not None and self.jumper.status == 1:
                self._status = 1
            else:
                self._status = 3
        else:
            self._status = status

    @property
    def users_list_byconnectip(self):
        if self._status != 1:
            return []
        else:
            return list(self.hosts.values_list('connect_ip', flat=True))

    @property
    def users_list_byhostname(self):
        return list(self.hosts.values_list('hostname', flat=True))


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
    id = models.AutoField(primary_key=True)#全局ID
    disk_size = models.CharField(max_length=100,default="")
    disk_path = models.CharField(max_length=100,default="")
    info = models.CharField(max_length=100,default="")

    def __unicode__(self):
        return self.disk_path + ' - ' + self.info

    __str__ = __unicode__

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
    position = models.ForeignKey(Position, on_delete=models.SET_NULL, null=True, related_name='hosts_detail')
    systemtype = models.ForeignKey(System_Type, on_delete=models.SET_NULL, null=True, related_name='hosts_detail')
    info = models.CharField(max_length=200, default="", null=True, blank=True)
    aliyun_id = models.CharField(max_length=30, default='', blank=True, null=True)
    vmware_id = models.CharField(max_length=36, default='', blank=True, null=True)


class Host(models.Model):
    SYSTEM_STATUS = (
        (0, '错误'),
        (1, '正常'),
        (2, '不可达'),
    )
    # 主机标识
    id = models.AutoField(primary_key=True) #全局ID

    # 资产结构
    groups = models.ManyToManyField(Group, null=True, blank=True, related_name='hosts', verbose_name=_("Host"))
    # 所属应用
    storages = models.ManyToManyField(Storage, blank=True, related_name='hosts', verbose_name=_('Host'))

    # 相关信息
    connect_ip = models.GenericIPAddressField(default='', null=False)
    service_ip = models.GenericIPAddressField(default='0.0.0.0', null=True)

    # 主机名称
    hostname = models.CharField(max_length=50, default='localhost.localdomain', null=True, blank=True)

    # 用户端口
    sshport = models.IntegerField(default='22')
    detail = models.ForeignKey(HostDetail, related_name='host', on_delete=models.SET_NULL, null=True)
    _passwd = models.CharField(max_length=1000, default='', null=True, blank=True)

    # 服务器状态
    _status = models.IntegerField(default=1, choices=SYSTEM_STATUS)

    class Meta:
        permissions = (
            ('yo_list_host', u'罗列主机'),
            ('yo_create_host', u'新增主机'),
            ('yo_update_host', u'修改主机'),
            ('yo_delete_host', u'删除主机'),
            ('yo_detail_host', u'详细查看主机'),
            ('yo_passwd_host', u'获取主机密码'),
            ('yo_webskt_host', u'远控主机')
        )

    def __unicode__(self):
        uuid = None
        if self.detail.aliyun_id:
            uuid = str(self.detail.aliyun_id)
        elif self.detail.vmware_id:
            uuid = str(self.detail.vmware_id)
        else:
            uuid = 'None'
        return uuid + '-' + self.detail.info


    __str__ = __unicode__

    @property
    def status(self):
        return self._status

    @status.setter
    def status(self,status):
        self._status = status

    @property
    def password(self):
        if self._passwd:
            return aes.decrypt(self._passwd)
        else:
            return 'nopassword'

    @password.setter
    def password(self, password):
        self._passwd = aes.encrypt(password.encode('utf-8'))

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