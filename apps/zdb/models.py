# -*- coding:utf-8 -*-
from __future__ import unicode_literals
from django.utils.translation import ugettext_lazy as _
from django.db import models
import uuid, socket
from manager.models import Group,Host
from deveops.utils import aes
from django.conf import settings
from zdb.tasks import status_flush

__all__ = [
    'Instance', 'InstanceGroup', "Database",
    "User"
]

class InstanceGroup(models.Model):
    id = models.AutoField(primary_key=True)
    uuid = models.UUIDField(auto_created=True, default=uuid.uuid4, editable=False)

    name = models.CharField(max_length=200, default='')
    group = models.OneToOneField(Group, related_name='dbgroup', on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        permissions = (
            ('yo_list_db_group', u'罗列数据库实例组'),
            ('yo_create_db_group', u'新增数据库实例组'),
            ('yo_update_db_group', u'修改数据库实例组'),
            ('yo_delete_db_group', u'删除数据库实例组'),
        )

    @property
    def status(self):
        status = settings.STATUS_DB_INSTANCE_CAN_BE_USE
        if self.instances.count() != 0:
            for instance in self.instances.all():
                status = instance.status and status
            return status
        else:
            return settings.STATUS_DB_INSTANCE_UNREACHABLE


    @property
    def group_name(self):
        if self.group is not None:
            return self.group.name
        else:
            return ""

    @property
    def instance_count(self):
        return self.instances.count()

    @property
    def database_count(self):
        count = 0
        for instance in self.instances.all():
            count = count + instance.databases.count()
        return count


class Instance(models.Model):
    INSTANCE_STATUS = (
        (settings.STATUS_DB_INSTANCE_PASSWORD_WRONG, '密码错误'),
        (settings.STATUS_DB_INSTANCE_CONNECT_REFUSE, '连接拒绝'),
        (settings.STATUS_DB_INSTANCE_UNREACHABLE, '不可到达'),
        (settings.STATUS_DB_INSTANCE_CAN_BE_USE, '正常'),
    )

    INSTANCE_TYPE = (
        (settings.TYPE_DB_INSTANCE_MASTER, '主节点'),
        (settings.TYPE_DB_INSTANCE_SLAVE, '子节点'),
        (settings.TYPE_DB_INSTANCE_MGR, 'MGR集群')
    )
    id = models.AutoField(primary_key=True)
    uuid = models.UUIDField(auto_created=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=200, default='')

    _connect_ip = models.CharField(max_length=300, default='', blank=True, null=True)
    port = models.IntegerField(default=3306)

    group = models.ForeignKey(InstanceGroup, related_name="instances", on_delete=models.SET_NULL, null=True, blank=True)

    # 阿里云RDS
    aliyun_id = models.CharField(max_length=30, default='', blank=True, null=True)

    # 私有云RDS
    host = models.ForeignKey(Host, related_name='dbinstance', on_delete=models.SET_NULL, null=True, blank=True)

    admin_user = models.CharField(default='root',max_length=100)
    _admin_passwd = models.CharField(max_length=1000, default='', null=True, blank=True)
    _status = models.IntegerField(default=settings.STATUS_DB_INSTANCE_UNREACHABLE, choices=INSTANCE_STATUS)

    type = models.IntegerField(default=settings.TYPE_DB_INSTANCE_MASTER, choices=INSTANCE_TYPE)


    class Meta:
        permissions = (
            ('yo_list_db', u'罗列数据库实例'),
            ('yo_create_db', u'新增数据库实例'),
            ('yo_update_db', u'修改数据库实例'),
            ('yo_delete_db', u'删除数据库实例'),
            ('yo_detail_db', u'详细查看数据库实例'),
            ('yo_passwd_db', u'获取数据库实例密码'),
        )

    def check_status(self):
        status_flush.delay(self)

    @property
    def status(self):
        return self._status

    @status.setter
    def status(self,status):
        self.check_status()

    @property
    def connect_ip(self):
        if self._connect_ip != '':
            return self._connect_ip
        else:
            return self.host.connect_ip

    @connect_ip.setter
    def connect_ip(self,connect_ip):
        self._connect_ip = connect_ip

    @property
    def group_name(self):
        return self.group.name

    @property
    def password(self):
        if self._admin_passwd:
            return aes.decrypt(self._admin_passwd)
        else:
            return ''

    @password.setter
    def password(self, password):
        self._admin_passwd = aes.encrypt(password).decode()


class Database(models.Model):
    id = models.AutoField(primary_key=True)
    uuid = models.UUIDField(auto_created=True, default=uuid.uuid4, editable=False)
    instance = models.ForeignKey(Instance, on_delete=models.SET_NULL, null=True, related_name='databases')
    info = models.CharField(max_length=1000, default='')


class User(models.Model):
    _passwd = models.CharField(max_length=1000, default='', null=True, blank=True)

    username = models.CharField(max_length=100, default='', null=False)
    src_address = models.CharField(max_length=15, default='', null=False)
    database = models.OneToOneField(Database, related_name='user', on_delete=models.SET_NULL, null=True, blank=True)

    # 权限

    @property
    def password(self):
        if self._passwd:
            return aes.decrypt(self._passwd)
        else:
            return 'nopassword'

    @password.setter
    def password(self, password):
        self._passwd = aes.encrypt(password).decode()

