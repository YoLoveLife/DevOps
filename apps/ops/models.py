# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
from django.utils.translation import ugettext_lazy as _
from manager.models import Group,Host

__all__ = [
    'META', 'META_CONTENT'
]


class META_CONTENT(models.Model):
    id = models.IntegerField(primary_key=True)
    module = models.CharField(default='',max_length=20)
    args = models.CharField(default='', max_length=100)
    sort = models.IntegerField(default=0)

    class Meta:
        permissions = (('yo_list_metacontent', u'罗列元操作内容'),
                       ('yo_create_metacontent', u'创建元操作内容'),
                       ('yo_update_metacontent',u'更新元操作内容'),
                       ('yo_delete_metacontent',u'删除元操作内容'))


class META(models.Model):
    id = models.IntegerField(primary_key=True)
    group = models.ForeignKey(Group, on_delete=models.SET_NULL, null=True, related_name='hosts_detail')
    hosts = models.ManyToManyField(Host, blank=True, related_name='metas', verbose_name=_("metas"))
    contents = models.ManyToManyField(META_CONTENT, blank=True, related_name='contents', verbose_name=_("contents"))

    class Meta:
        permissions = (('yo_list_meta', u'罗列元操作'),
                       ('yo_create_meta', u'创建元操作'),
                       ('yo_update_meta',u'更新元操作'),
                       ('yo_delete_meta',u'删除元操作'))


