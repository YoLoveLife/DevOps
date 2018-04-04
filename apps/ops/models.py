# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.core.exceptions import ObjectDoesNotExist
from manager.models import Group,Host
import uuid

__all__ = [
    'META', 'META_CONTENT',
    'Mission', 'Push_Mission'
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
    # 指定某幾台主機進行操作的元操作
    id = models.IntegerField(primary_key=True)
    uuid = models.UUIDField(auto_created=True, default=uuid.uuid4, editable=False)
    group = models.ForeignKey(Group, on_delete=models.SET_NULL, null=True, related_name='group_metas')
    # 當hosts為空 則說明該meta任務為本地執行
    hosts = models.ManyToManyField(Host, blank=True, null=True, related_name='user_metas', verbose_name=_("metas"))
    info = models.CharField(default='', max_length=5000)
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
        obj = {}
        for host in self.hosts.all():
            hosts_list.append(host.connect_ip)
        if len(hosts_list) == 0:
            for content in self.contents.all():
                tasks.append(content.to_yaml)
            obj = {
                'tasks': tasks,
                'gather_facts': 'no',
                'hosts': 'localhost',
            }
        else:
            try:
                jumper = self.group.jumper
                proxy_task = {
                                 u'set_fact':
                                     {
                                         'ansible_ssh_common_args':
                                             '-o ProxyCommand="ssh -p{PORT} -W %h:%p root@{IP}"'.format(PORT=jumper.sshport, IP=jumper.connect_ip)
                                     }
                             }
                tasks.append(proxy_task)
                for content in self.contents.all():
                    tasks.append(content.to_yaml)
                obj = {
                    'tasks': tasks,
                    'gather_facts': 'no',
                    'hosts': ','.join(hosts_list)+',',
                }
            except ObjectDoesNotExist:
                pass
        return obj


class Mission(models.Model):
    VALIDATE = (
        (0, '需要验证'),
        (1, '不需要验证')
    )

    class Meta:
        permissions = (('yo_list_mission', u'罗列任务'),
                       ('yo_create_mission', u'创建任务'),
                       ('yo_update_mission', u'更新任务'),
                       ('yo_delete_mission', u'删除任务'))

    id = models.IntegerField(primary_key=True)
    metas = models.ManyToManyField(META,blank=True,related_name='missions',verbose_name=_("Mission"))
    info = models.CharField(default='',max_length=5000)
    need_validate = models.IntegerField(choices=VALIDATE, default=0)


class Push_Mission(models.Model):
    VALIDATE = (
        (0, '未验证'),
        (1, '已验证')
    )
    DONE = (
        (0, '未完成'),
        (1, '已完成'),
        (2, '出错')
    )

    class Meta:
        permissions = (('yo_list_pushmission', u'罗列推出任务'),
                       ('yo_create_pushmission', u'创建推出任务'))

    id = models.IntegerField(primary_key=True)
    # 由哪個Mission推送出來的任務
    mission = models.ForeignKey(Mission, related_name='push_missions')
    # 是否通過驗證 該值由Mission的need_validate來初始化
    _validate = models.IntegerField(choices=VALIDATE, default=0)
    _done = models.IntegerField(choices=DONE, default=0)
    # 任務推出時間
    create_time = models.DateTimeField(auto_now_add=True)
    # 任務結束時間
    finish_time = models.DateTimeField(auto_now=True)

    @property
    def done(self):
        return self._done

    @done.setter
    def done(self, done):
        self._done = done

    @property
    def validate(self):
        return self._validate

    @validate.setter
    def validate(self, validate):
        self._validate = validate

