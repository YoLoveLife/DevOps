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
    uuid = models.UUIDField(auto_created=True, default=uuid.uuid4, editable=False)
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
        FIND_LABLE="file:"
        if self.need_file == True and self.args.find(FIND_LABLE)!=-1:
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
            return file_name[0][2:-2]
        else:
            return ''


class META(models.Model):
    # 指定某幾台主機進行操作的元操作
    id = models.AutoField(primary_key=True)
    uuid = models.UUIDField(auto_created=True, default=uuid.uuid4, editable=False)
    group = models.ForeignKey(Group, on_delete=models.SET_NULL, null=True, related_name='group_metas')
    # 當hosts為空 則說明該meta任務為本地執行
    hosts = models.ManyToManyField(Host, blank=True, related_name='user_metas', verbose_name=_("metas"))
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
            if content.need_file is True and content.file_name != "":
                files.append(content.file_name)
        return files

    @property
    def to_yaml(self):
        tasks = []
        hosts_list = []
        obj = {}
        for host in self.hosts.all():
            if host._status == 1:
                hosts_list.append(host.connect_ip)
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
    uuid = models.UUIDField(auto_created=True, default=uuid.uuid4, editable=False)
    group = models.ForeignKey(Group, on_delete=models.SET_NULL, null=True, related_name='group_missions')
    metas = models.ManyToManyField(META,blank=True, related_name='missions', verbose_name=_("Mission"))
    info = models.CharField(default='', max_length=5000)
    need_validate = models.BooleanField(default=True)

    @property
    def file_list(self):
        list = []
        for meta in self.metas.all():
            if len(meta.file_list) !=0 :
                list = list + meta.file_list
        return list

    @property
    def vars_dict(self):
        dict = {}
        vars = self.group.group_vars
        for var in vars:
            dict[var.key] = var.value
        return dict

    @property
    def to_yaml(self):
        list = []
        for meta in self.metas.all():
            list.append(meta.to_yaml)
        return list

    @property
    def count(self):
        return self.push_missions.count()

    @property
    def playbook(self):
        import yaml
        return yaml.safe_dump_all(self.to_yaml)

    def model_to_dict(self):
        from django.forms.models import model_to_dict
        return model_to_dict(self)


class META_SORT(models.Model):
    # 针对meta的排序
    id = models.AutoField(primary_key=True)
    uuid = models.UUIDField(auto_created=True, default=uuid.uuid4, editable=False)
    mission = models.ForeignKey(Mission, on_delete=models.SET_NULL, null=True, related_name='sort')
    meta = models.ForeignKey(META, on_delete=models.SET_NULL, null=True, related_name='sort')
    sort = models.IntegerField(default=1)


class Push_Mission(models.Model):
    STATUS = (
        (0, '审核工单'), # 未审核
        (1, '上传文件'), # 未上传文件
        (2, '执行工单'), # 未执行
        (3, '执行中'), # 执行中
        (4, '执行完毕'), # 执行完毕
    )

    class Meta:
        permissions = (('yo_list_pushmission', u'罗列推出任务'),
                       ('yo_create_pushmission', u'创建推出任务'))

    id = models.AutoField(primary_key=True)
    uuid = models.UUIDField(auto_created=True, default=uuid.uuid4, editable=False)
    # 由哪個Mission推送出來的任務
    mission = models.ForeignKey(Mission, related_name='push_missions', null=True, on_delete=models.SET_NULL)
    # 推出任务状态
    _status = models.IntegerField(choices=STATUS, default=0)
    # 任務推出時間
    create_time = models.DateTimeField(auto_now_add=True)
    # 任務結束時間
    finish_time = models.DateTimeField(auto_now=True)
    # 執行內容
    results = models.CharField(default='', max_length=5000)
    # 关联文件
    files = models.ManyToManyField(FILE, related_name='pushs', blank=True)

    @property
    def status(self):
        return self._status

    @status.setter
    def status(self, status):
        self._status = status


