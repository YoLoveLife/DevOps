# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
from django.utils.translation import ugettext_lazy as _
from manager.models import Group,Host
import uuid

__all__ = [
    'META', 'META_CONTENT'
]


class META_CONTENT(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=50, default='')
    module = models.CharField(default='',max_length=20)
    args = models.CharField(default='', max_length=100)
    sort = models.IntegerField(default=0)

    class Meta:
        permissions = (('yo_list_metacontent', u'罗列元操作内容'),
                       ('yo_create_metacontent', u'创建元操作内容'),
                       ('yo_update_metacontent', u'更新元操作内容'),
                       ('yo_delete_metacontent', u'删除元操作内容'))

    @property
    def to_yaml(self):
        return {
            self.module: self.args, 'name': self.name
        }


class META(models.Model):
    id = models.IntegerField(primary_key=True)
    uuid = models.UUIDField(auto_created=True, default=uuid.uuid4, editable=False)
    group = models.ForeignKey(Group, on_delete=models.SET_NULL, null=True, related_name='hosts_detail')
    hosts = models.ManyToManyField(Host, blank=True, related_name='metas', verbose_name=_("metas"))
    info = models.CharField(default='',max_length=5000)
    contents = models.ManyToManyField(META_CONTENT, blank=True, related_name='contents', verbose_name=_("contents"))

    class Meta:
        permissions = (('yo_list_meta', u'罗列元操作'),
                       ('yo_create_meta', u'创建元操作'),
                       ('yo_update_meta', u'更新元操作'),
                       ('yo_delete_meta', u'删除元操作'))

    @property
    def to_yaml(self):
        tasks = []
        hosts_list = []
        for host in self.hosts.all():
            hosts_list.append(host.connect_ip)
        for content in self.contents.all():
            tasks.append(content.to_yaml)
        return {
            'tasks': tasks,
            'gather_facts': 'no',
            'hosts': ','.join(hosts_list),
        }

