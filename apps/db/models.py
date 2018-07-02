# -*- coding:utf-8 -*-
from __future__ import unicode_literals
from django.utils.translation import ugettext_lazy as _
from django.db import models
from authority.models import ExtendUser
import uuid
from manager.models import Group,Host,Position
from deveops.utils import aes

__all__ = [
    'Instance', 'User', 'Role'
]


class Instance(models.Model):
    INSTANCE_STATUS = (
        (0, '错误'),
        (1, '正常'),
    )
    id = models.AutoField(primary_key=True)
    uuid = models.UUIDField(auto_created=True, default=uuid.uuid4, editable=False)
    # 关联的主机
    aliyun_id = models.CharField(max_length=30, default='', blank=True, null=True)
    group = models.ForeignKey(Group, default=None, blank=True, null=True, on_delete=models.SET_NULL)
    hosts = models.ManyToManyField(Host, blank=True, related_name='dbs', verbose_name=_("dbs"))
    name = models.CharField(max_length=100, default='')
    port = models.IntegerField(default=3306)
    is_master = models.BooleanField(default=True)
    admin_user = models.CharField(default='root',max_length=100)
    # position = models.ForeignKey(Position, on_delete=models.SET_NULL, null=True, related_name='instances')
    _admin_passwd = models.CharField(max_length=1000, default='', null=True, blank=True)
    _status = models.IntegerField(default=0, choices=INSTANCE_STATUS)

    class Meta:
        permissions = (
            ('yo_list_db', u'罗列数据库实例'),
            ('yo_create_db', u'新增数据库实例'),
            ('yo_update_db', u'修改数据库实例'),
            ('yo_delete_db', u'删除数据库实例'),
            ('yo_detail_db', u'详细查看数据库实例'),
            ('yo_passwd_db', u'获取数据库实例密码'),
        )

    @property
    def status(self):
        return self._status

    @status.setter
    def status(self,status):
        self._status = status

    @property
    def password(self):
        if self._admin_passwd:
            return aes.decrypt(self._admin_passwd)
        else:
            return 'nopassword'

    @password.setter
    def password(self, password):
        self._admin_passwd = aes.encrypt(password).decode()

    @property
    def group_name(self):
        if self.group is not None:
            return self.group.name
        else:
            return ""


class Role(models.Model):
    ROLE_PERMISSIONS_STR_NUMBER = {
        'select': 1,
        'update': 2,
        'delete': 3,
        'insert': 4,
        'create': 5,
        'drop': 6,
        'alter': 7,
    }
    ROLE_PERMISSIONS_NUMBER_STR = {
        1:'select',
        2:'update',
        3:'delete',
        4:'insert',
        5:'create',
        6:'drop',
        7:'alter',
    }
    id = models.AutoField(primary_key=True)
    uuid = models.UUIDField(auto_created=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=50, default="")
    info = models.CharField(max_length=50, default="")
    instance = models.ForeignKey(Instance, default=None, null=True, on_delete=models.SET_NULL, related_name="roles")
    can_select = models.BooleanField(default=False)
    can_update = models.BooleanField(default=False)
    can_delete = models.BooleanField(default=False)
    can_insert = models.BooleanField(default=False)
    can_create = models.BooleanField(default=False)
    can_drop = models.BooleanField(default=False)
    can_alter = models.BooleanField(default=False)

    class Meta:
        permissions = (
            ('yo_list_db_role', u'罗列数据库角色'),
            ('yo_create_db_role', u'新增数据库角色'),
            ('yo_update_db_role', u'修改数据库角色'),
            ('yo_delete_db_role', u'删除数据库角色'),
        )

    @property
    def group_name(self):
        if self.instance is not None:
            return self.instance.group_name
        else:
            return ""

    def reset_permission(self):
        for permission in self.ROLE_PERMISSIONS_STR_NUMBER:
            setattr(self,'can_'+permission, False)

    @property
    def permission_list(self):
        l = []
        for item in self.__dict__.keys():
            if getattr(self,item) is True:
                l.append(self.ROLE_PERMISSIONS_STR_NUMBER[item[4:]])
        return l

    @permission_list.setter
    def permission_list(self,permissions):
        self.reset_permission()
        for permission in permissions:
            setattr(self,'can_'+self.ROLE_PERMISSIONS_NUMBER_STR[permission], True)


    @property
    def permissions_str(self):
        return ','.join(self.permission_list)


class User(models.Model):
    USER_STATUS = (
        (0, '禁用'),
        (1, '正常'),
    )
    id = models.AutoField(primary_key=True)
    uuid = models.UUIDField(auto_created=True, default=uuid.uuid4, editable=False)
    username = models.CharField(null=False,max_length=20)
    role = models.ForeignKey(Role, default=None, blank=True, null=True, on_delete=models.SET_NULL, related_name='users')
    _passwd = models.CharField(max_length=1000, default='', null=True, blank=True)
    _status = models.IntegerField(default=0, choices=USER_STATUS)
    info = models.CharField(default="",max_length=100)

    class Meta:
        permissions = (
            ('yo_list_db_user', u'罗列数据库用户'),
            ('yo_create_db_user', u'新增数据库用户'),
            ('yo_update_db_user', u'修改数据库用户'),
            ('yo_delete_db_user', u'删除数据库用户'),
            ('yo_passwd_db_user', u'获取数据库实例用户'),
        )

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
        self._passwd = aes.encrypt(password).decode()


    @property
    def role_info(self):
        if self.role is not None:
            return self.role.info
        else:
            return ""

    @property
    def group_name(self):
        if self.role is not None:
            return self.role.group_name
        else:
            return ""

