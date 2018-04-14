# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.core.exceptions import ObjectDoesNotExist
from manager.models import Group,Host
from utils.models import FILE
from django.conf import settings
import os
import uuid

__all__ = [
    'META', 'META_CONTENT',
    'Mission', 'Push_Mission'
]


class META_CONTENT(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50, default='')
    module = models.CharField(default='',max_length=20)
    args = models.CharField(default='', max_length=100)
    sort = models.IntegerField(default=0)
    need_file = models.BooleanField(default=False)

    class Meta:
        permissions = (('yo_list_metacontent', u'罗列元操作内容'),
                       ('yo_create_metacontent', u'创建元操作内容'),
                       ('yo_update_metacontent', u'更新元操作内容'),
                       ('yo_delete_metacontent', u'删除元操作内容'))

    @property
    def args_clean(self):
        if self.need_file == True:
            args_list = self.args.split('file:')
            return args_list[0]+args_list[1]
        else:
            return self.args

    @property
    def to_yaml(self):
        return {
            self.module: self.args_clean, 'name': self.name
        }

    @property
    def file_name(self):
        FIND_LABLE="file:"
        if self.need_file == True and self.args.find(FIND_LABLE)!=-1:
            args_list = self.args.split(FIND_LABLE)
            file_name = args_list[1].split(' ')
            return file_name[0]
        else:
            return ''


class META(models.Model):
    # 指定某幾台主機進行操作的元操作
    id = models.AutoField(primary_key=True)
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
    def file_list(self):
        files = []
        for content in self.contents.all():
            if content.need_file == True and content.file_name!="":
                files.append(content.file_name)
        return files

    @property
    def to_yaml(self):
        tasks = []
        hosts_list = []
        obj = {}
        for host in self.hosts.all():
            hosts_list.append(host.connect_ip)
            print(hosts_list)
        if len(hosts_list) == 0:
            # 主机列表为空说明本地执行
            for content in self.contents.all().order_by('sort'):
                tasks.append(content.to_yaml)
            obj = {
                'tasks': tasks,
                'gather_facts': 'no',
                'hosts': 'localhost',
            }
        else:
            jumper = self.group.jumper
            if jumper is not None:
                proxy_task = {
                                 u'set_fact':
                                     {
                                         'ansible_ssh_common_args':
                                             '-o ProxyCommand="ssh -p{PORT} -W %h:%p root@{IP}"'.format(PORT=jumper.sshport, IP=jumper.connect_ip)
                                     }
                             }
                tasks.append(proxy_task)
                for content in self.contents.all().order_by('sort'):
                    tasks.append(content.to_yaml)
                obj = {
                    'tasks': tasks,
                    'gather_facts': 'no',
                    'hosts': ','.join(hosts_list)+',',
                }
        return obj


class Mission(models.Model):
    class Meta:
        permissions = (('yo_list_mission', u'罗列任务'),
                       ('yo_create_mission', u'创建任务'),
                       ('yo_update_mission', u'更新任务'),
                       ('yo_delete_mission', u'删除任务'))
    id = models.AutoField(primary_key=True)
    group = models.ForeignKey(Group, on_delete=models.SET_NULL, null=True, related_name='group_missions')
    metas = models.ManyToManyField(META,blank=True, related_name='missions', verbose_name=_("Mission"))
    info = models.CharField(default='', max_length=5000)
    need_validate = models.BooleanField(default=True)

    @property
    def file_list(self):
        list = []
        for meta in self.metas.all():
            list = list + meta.file_list
        return list

    @property
    def to_yaml(self):
        list = []
        for meta in self.metas.all():
            list.append(meta.to_yaml)
        return list

    def model_to_dict(self):
        from django.forms.models import model_to_dict
        return model_to_dict(self)


class META_SORT(models.Model):
    # 针对meta的排序
    id = models.AutoField(primary_key=True)
    mission = models.ForeignKey(Mission, on_delete=models.SET_NULL, null=True, related_name='sort')
    meta = models.ForeignKey(META, on_delete=models.SET_NULL, null=True, related_name='sort')
    sort = models.IntegerField(max_length=5,default=1)


class Push_Mission(models.Model):
    DONE = (
        (0, '未完成'),
        (1, '已完成'),
        (2, '出错')
    )

    class Meta:
        permissions = (('yo_list_pushmission', u'罗列推出任务'),
                       ('yo_create_pushmission', u'创建推出任务'))

    id = models.AutoField(primary_key=True)
    # 由哪個Mission推送出來的任務
    uuid = models.UUIDField(auto_created=True, default=uuid.uuid4, editable=False)
    mission = models.ForeignKey(Mission, related_name='push_missions')
    # 是否通過驗證 該值由Mission的need_validate來初始化
    _validate = models.BooleanField(default=False)
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


