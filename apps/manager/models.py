# -*- coding:utf-8 -*-
# !/usr/bin/env python
# Time 17-10-25
# Author Yo
# Email YoLoveLife@outlook.com
from django.utils.translation import ugettext_lazy as _
from django.db import models
import uuid
from authority.models import ExtendUser
from deveops.utils import sshkey, aes
from utils.models import IMAGE
from django.contrib.auth.models import Group as PerGroup
from authority.models import Key, Jumper
from django.conf import settings

__all__ = [
    "Group", "Host"
]


class Group(models.Model):
    id = models.AutoField(primary_key=True)
    uuid = models.UUIDField(auto_created=True, default=uuid.uuid4, editable=False)

    name = models.CharField(max_length=100, default='')
    info = models.CharField(max_length=100, default='')
    _framework = models.ForeignKey(IMAGE, related_name='groups', on_delete=models.SET_NULL, null=True)
    # 超级管理员
    users = models.ManyToManyField(ExtendUser, blank=True, related_name='assetgroups', verbose_name=_("assetgroups"))
    pmn_groups = models.ManyToManyField(PerGroup, blank=True, related_name='assetgroups', verbose_name=_("assetgroups"))

    # 操作凭证
    key = models.OneToOneField(Key, related_name='group', on_delete=models.SET_NULL, null=True, blank=True)
    jumper = models.OneToOneField(Jumper, related_name='group', on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        permissions = (('yo_list_group', u'罗列应用组'),
                       ('yo_create_group', u'新增应用组'),
                       ('yo_update_group', u'修改应用组'),
                       ('yo_detail_group', u'详细查看应用组'),
                       ('yo_delete_group', u'删除应用组'),
                       ('yo_group_sort_host', u'批量归类主机'))

    @property
    def status(self):
        if self.jumper is None or self.key is None:
            return settings.STATUS_GROUP_UNREACHABLE
        elif self.jumper is not None and self.key is not None:
            if self.jumper.status == settings.STATUS_JUMPER_CAN_BE_USE:
                return settings.STATUS_GROUP_CAN_BE_USE
            else:
                return settings.STATUS_GROUP_PAUSE

    @status.setter
    def status(self, status):
        if self.jumper is not None:
            self.jumper.check_status()
        else:
            pass

    def framework_update(self):
        if not self._framework is None:
            self._framework.delete()
        return True

    @property
    def framework(self):
        return self._framework.file

    @framework.setter
    def framework(self, framework):
        self._framework = framework

    @property
    def users_list_byconnectip(self):
        if self.status != settings.STATUS_GROUP_CAN_BE_USE:
            return []
        else:
            # Ansible 2.0.0.0
            # return list(self.hosts.values_list('connect_ip', flat=True)) Only Normal Host
            return ','.join(list(self.hosts.filter(_status__gte=0).values_list('connect_ip', flat=True)))

    @property
    def vars_dict(self):
        var_dict = {}
        for var in self.vars.all():
            var_dict[var.key] = var.value
        var_dict['JUMPER_IP'] = self.jumper.connect_ip
        var_dict['JUMPER_PORT'] = self.jumper.sshport
        return var_dict


class Host(models.Model):
    # 主机标识
    id = models.AutoField(primary_key=True) # 全局ID
    uuid = models.UUIDField(auto_created=True, default=uuid.uuid4, editable=False)

    # 资产结构
    groups = models.ManyToManyField(Group, blank=True, related_name='hosts', verbose_name=_("Host"))

    # 连接信息
    connect_ip = models.CharField(max_length=15, default='', null=False)
    sshport = models.IntegerField(default='22')
    _passwd = models.CharField(max_length=1000, default='', null=True, blank=True)

    # 主机信息
    hostname = models.CharField(max_length=50, default='localhost.localdomain', null=True, blank=True)
    aliyun_id = models.CharField(max_length=30, default='', blank=True, null=True)
    vmware_id = models.CharField(max_length=36, default='', blank=True, null=True)
    info = models.CharField(max_length=200, default="", null=True, blank=True)
    position = models.CharField(max_length=50, default="")
    systemtype = models.CharField(max_length=50, default="")

    # 服务器状态
    _status = models.IntegerField(default=1,)

    class Meta:
        permissions = (
            ('yo_list_host', u'罗列主机'),
            ('yo_create_host', u'新增主机'),
            ('yo_update_host', u'修改主机'),
            ('yo_delete_host', u'删除主机'),
            ('yo_host_sort_group', u'更改主机应用组'),
            ('yo_passwd_host', u'获取主机密码'),
            ('yo_webskt_host', u'远控主机')
        )

    @property
    def status(self):
        if not self.groups.exists():
            return settings.STATUS_HOST_NOT_SELECT
        return self._status

    @status.setter
    def status(self, status):
        if self._status == settings.STATUS_HOST_PAUSE or self._status == settings.STATUS_HOST_CAN_BE_USE:
            self._status = status
        if status == settings.STATUS_HOST_PAUSE:
            self._status = status
        return

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
    def group(self):
        group_list = []
        for group in self.groups.all():
            group_list.append(group.name)
        return ';'.join(group_list)

    # :TODO 详细页面 管理用户
    def manage_user_get(self):
        pass
