# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import Group
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import AbstractUser

__all__ = [
    "ExtendUser"
]

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

    @property
    def is_oper(self):
        if self.groups.filter(name__icontains='运维').count() != 0:
            return True
        return False

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