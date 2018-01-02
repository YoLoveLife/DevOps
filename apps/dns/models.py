# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
from django.utils.translation import gettext_lazy as _
from manager.models import Group
# Create your models here.
class DNS(models.Model):
    id = models.AutoField(primary_key=True)#全局ID
    sons = models.ManyToManyField('self',blank=True,related_name='DNSfather',verbose_name=_("sons")) #子节点
    group = models.ForeignKey(Group,related_name='dns',verbose_name=_("group"),blank=True) #所属应用组
    name = models.CharField(max_length=100,default='')
