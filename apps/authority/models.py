# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import Permission,Group
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import AbstractUser

# class ExtendGroup(Group):
#     phone = models.CharField(max_length=11,default='None',)
#     def get_permissions(self):
#         str = ""
#         permissions = self.permissions.all()
#         for permission in permissions:
#             str += permission.name + ' '
#         return str

class ExtendUser(AbstractUser):
    img = models.CharField(max_length=10,default='user.jpg')
    phone = models.CharField(max_length=11,default='None',)
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


    def __unicode__(self):
        str = ""
        print(self.groups.all())
        for group in self.groups.all():
            str += '/'+group.name
        return self.username +' - '+ str

    __str__ = __unicode__

    def get_8531email(self):
        return self.email.split('@')[0] + '@8531.cn'

    def get_full_name(self):
        """
        Returns the first_name plus the last_name, with a space in between.
        """
        full_name = '%s' % (self.last_name,)# self.first_name)
        return full_name.strip()

    def get_group_name(self):
        """
        :return: Name of group
        """
        if self.is_superuser == 1:
            return "超级管理员"
        elif self.groups.count() == 0:
            return "无权限"
        else:
            str = ""
            groups = self.groups.all()
            for group in groups:
                str += group.name + ' '
            return str