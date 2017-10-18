# -*- coding:utf-8 -*-
from __future__ import unicode_literals


from django.db import models
from django.shortcuts import reverse
from django.contrib.auth.models import AbstractUser
from django.utils.translation import ugettext_lazy as _
# from authority.models import PermissionGroup
# Create your models here.

class ExtendUser(AbstractUser):
    img = models.CharField(max_length=10,default='user.jpg')
    phone = models.CharField(max_length=11,default='18458409298',)
    # groups = models.ManyToManyField(
    #     PermissionGroup,
    #     verbose_name=_('groups'),
    #     blank=True,
    #     help_text=_(
    #         'The groups this user belongs to. A user will get all permissions '
    #         'granted to each of their groups.'
    #     ),
    #     related_name="user_set",
    #     related_query_name="user",
    # )

    def get_full_name(self):
        """
        Returns the first_name plus the last_name, with a space in between.
        """
        full_name = '%s%s' % (self.first_name, self.last_name)
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
