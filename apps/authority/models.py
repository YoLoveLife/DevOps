# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import Group
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from deveops.utils import sshkey,aes
import django.utils.timezone as timezone

__all__ = [
    "Key", "ExtendUser"
]

def private_key_validator(key):
    if not sshkey.private_key_validator(key):
        raise ValidationError(
            _('%(value)s is not an even number'),
            params={'value': key},
        )


class Key(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, default='')

    # 操作权限限定
    _private_key = models.TextField(max_length=4096, blank=True, null=True, validators=[private_key_validator])
    _public_key = models.TextField(max_length=4096, blank=True, null=True)
    # 使用时间
    _fetch_time = models.DateTimeField(default=timezone.now)

    class Meta:
        permissions = (
            ('yo_list_key', u'罗列密钥'),
            ('yo_create_key', u'创建密钥'),
            ('yo_update_key', u'更新密钥'),
            ('yo_delete_key', u'删除密钥'),
        )

    @property
    def private_key(self):
        if self._private_key:
            key_str = aes.decrypt(self._private_key)
            return key_str
        else:
            return None

    @private_key.setter
    def private_key(self, private_key):
        self._private_key = aes.encrypt(private_key.encode('utf-8'))

    @property
    def public_key(self):
        return aes.decrypt(self._public_key)

    @public_key.setter
    def public_key(self, public_key):
        self._public_key = aes.encrypt(public_key.encode('utf-8'))

    @property
    def fetch_time(self):
        return self._fetch_time

    @fetch_time.setter
    def fetch_time(self, fetch_time):
        if fetch_time:
            self._fetch_time = timezone.now

    @property
    def group_name(self):
        if self.group.exists():
            return self.group.get().name
        else:
            return u'未指定'

class ExtendUser(AbstractUser):
    img = models.CharField(max_length=10, default='user.jpg')
    phone = models.CharField(max_length=11, default='None',)
    full_name = models.CharField(max_length=11, default='未获取')
    groups = models.ManyToManyField(
        Group,
        verbose_name=_('groups'),
        blank=True,
        help_text=_(
            'The groups this user belongs to. A user will get all permissions '
            'granted to each of their groups.'
        ),
        related_name="user_set",
        related_query_name="user",
    )

    class Meta:
        permissions = (
            ('yo_list_user', u'罗列用户'),
            ('yo_list_opsuser', u'罗列运维用户'),
            ('yo_create_user', u'新增用户'),
            ('yo_update_user', u'修改用户'),
            ('yo_delete_user', u'删除用户'),
            ('yo_list_pmngroup', u'罗列权限组'),
            ('yo_create_pmngroup', u'新增权限组'),
            ('yo_update_pmngroup', u'修改权限组'),
            ('yo_delete_pmngroup', u'删除权限组'),
            # django.contrib.auth.models.Permission django.contrib.auth.models.Group 无法重构
            ('yo_list_permission', u'罗列所有权限')
        )

    def __unicode__(self):
        list = []
        if self.is_superuser:
            list.append(u'超级管理员')
        elif self.groups.count() == 0:
            list.append(u'无权限')
        else:
            for group in self.groups.all():
                list.append(group.name)
        return self.username + ' - ' + "|".join(list)

    __str__ = __unicode__

    def get_8531email(self):
        return self.username + '@8531.cn'

    def get_group_name(self):
        if self.is_superuser == 1:
            return "超级管理员"
        elif self.groups.count() == 0:
            return "无权限"
        else:
            str = "|"
            list = []
            groups = self.groups.all()
            for group in groups:
                list.append(group.name)
            if len(list) == 0:
                return ''
            else:
                return str.join(list)