# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
from django.utils.translation import gettext_lazy as _
from manager.models import Group
import uuid
# Create your models here.

class DNS(models.Model):
    id = models.AutoField(primary_key=True)#全局ID
    uuid = models.UUIDField(auto_created=True, default=uuid.uuid4, editable=False)
    father = models.ForeignKey('self', blank=True, related_name='sons', verbose_name=_("father"), null=True, on_delete=models.SET_NULL) #父亲节点
    group = models.ForeignKey(Group,related_name='dns',verbose_name=_("group"), blank=True, null=True, on_delete=models.SET_NULL) #所属应用组
    name = models.CharField(max_length=100, default='')
    inner_dig = models.CharField(max_length=100, default='')
    dig = models.CharField(max_length=100, default='')

    class Meta:
        permissions = (
            ('yo_list_dns', u'罗列域名'),
            ('yo_create_dns', u'新增域名'),
            ('yo_update_dns', u'修改域名'),
            ('yo_detail_dns', u'详细查看域名'),
            ('yo_delete_dns', u'删除域名'),
        )

    def __unicode__(self):
        root_name = ""
        if self.father is not None:
            return self.recursion_name()
        if root_name == "":
            return self.name
        return root_name

    __str__ = __unicode__

    def recursion_name(self):
        if self.father is not None:
            return self.name + '.' + self.father.recursion_name()
        else:
            return self.name

    @property
    def level(self):
        if self.father is not None:
            return self.recursion_level()
        return 1

    def recursion_level(self):
        if self.father is not None:
            return 1 + self.father.recursion_level()
        else:
            return 1


