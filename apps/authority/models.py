# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import Permission,Group
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.utils import sshkey
from django.utils import aes
def private_key_validator(key):
    if not sshkey.private_key_validator(key):
        raise ValidationError(
            _('%(value)s is not an even number'),
            params={'value': key},
        )

class Root_User(models.Model):
    BECOME_METHOD_CHOICES = (
        ('sudo', 'sudo'),
        ('su', 'su'),
    )
    id = models.IntegerField(primary_key=True)
    username = models.CharField(max_length=64)
    __password = models.CharField(max_length=256,blank=True,null=True)
    __private_key = models.TextField(max_length=4096,blank=True,null=True,validators=[private_key_validator])
    __public_key = models.TextField(max_length=4096,blank=True)
    become = models.BooleanField(default=True)
    become_method = models.CharField(choices=BECOME_METHOD_CHOICES,default='sudo',max_length=4)
    become_user = models.CharField(default='root',max_length=16)
    become_pass = models.CharField(default='',max_length=128)

    def __unicode__(self):
        return self.username

    __str__ = __unicode__

    @property
    def password(self):
        if self.__password:
            return aes.decrypt(self.__password)
        else:
            return ''

    @password.setter
    def password(self,passwd):
        self.__password = aes.encrypt(passwd)

    @property
    def private_key(self):
        if self.__private_key:
            key_str = aes.decrypt(self.__private_key)
            return sshkey.ssh_private_key2obj(key_str)
        else:
            return None

    @private_key.setter
    def private_key(self,pri_key):
        self._private_key = aes.encrypt(pri_key)

    @property
    def public_key(self):
        return aes.decrypt(self.__public_key)

    @public_key.setter
    def public_key(self, pub_key):
        self._public_key = aes.encrypt(pub_key)

class Normal_User(models.Model):



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
        str = "|"
        list = []
        if self.is_superuser == True:
            list.append(u'超级管理员')
        elif self.groups.count() == 0:
            list.append(u'无权限')
        else:
            for group in self.groups.all():
                list.append(group.name)
        return self.username +' - '+ str.join(list)

    __str__ = __unicode__

    def get_8531email(self):
        return self.email.split('@')[0] + '@8531.cn'

    def get_full_name(self):
        """
        Returns the first_name plus the last_name, with a space in between.
        """
        full_name = '%s' % (self.last_name,)# self.first_name)
        return full_name.strip()

    @property
    def is_operationE(self):
        for group in self.groups.all():
            if group.id == 1:
                return True
        return False

    def get_group_name(self):
        """
        :return: Name of group
        """
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