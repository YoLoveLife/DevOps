# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.core.exceptions import ObjectDoesNotExist
from manager.models import Group, Host
from authority.models import ExtendUser
from utils.models import FILE
from django.conf import settings
from django_mysql.models import JSONField
import uuid, yaml

__all__ = [
    'META',
    'Mission', 'Push_Mission'
]


def null_tasks():
    return {
        'tasks': [],
    }


class TASKS(models.Model):
    _tasks = JSONField(default=null_tasks)

    class Meta:
        abstract = True

    @property
    def tasks(self):
        return yaml.dump(self._tasks, default_flow_style=False)

    @tasks.setter
    def tasks(self, tasks):
        self._tasks = yaml.load(tasks)

    def to_yaml(self, proxy):
        tasks = self._tasks
        print('AAA', tasks)
        for t in tasks['tasks']:
            for key, value in t.items():
                if key == 'copy':
                    t[key] = value.replace('<file>', '')
        tasks['tasks'].insert(0, proxy)
        return tasks

    def file_list(self):
        FIND_LABEL = '<file>'
        files = []
        for task in self._tasks.get('tasks'):
            if task.get('copy') is not None:
                if "<file>" in task.get('copy'):
                    copy_list = task.get('copy').split(FIND_LABEL)
                    file_name = copy_list[1].split(' ')
                    files.append(file_name[0][2:-2])
        return files


class META(TASKS):
    # 指定某幾台主機進行操作的元操作
    id = models.AutoField(primary_key=True)
    uuid = models.UUIDField(auto_created=True, default=uuid.uuid4, editable=False)
    group = models.ForeignKey(Group, on_delete=models.SET_NULL, null=True, related_name='group_metas')
    # 當hosts為空 則說明該meta任務為本地執行
    hosts = models.ManyToManyField(Host, blank=True, related_name='user_metas', verbose_name=_("metas"))
    info = models.CharField(default='', max_length=5000)
    facts = models.BooleanField(default=False)
    level = models.IntegerField(default=1)

    class Meta:
        ordering = [
            'level', 'id'
        ]
        permissions = (('yo_list_meta', u'罗列元操作'),
                       ('yo_create_meta', u'创建元操作'),
                       ('yo_update_meta', u'更新元操作'),
                       ('yo_delete_meta', u'删除元操作'))

    def file_list(self):
        return super(META, self).file_list()

    def gather_facts(self):
        if self.facts is True:
            return 'yes'
        else:
            return 'no'

    def to_yaml(self):
        proxy = {}
        hosts_list = []
        for host in self.hosts.all():
            if host.status == settings.STATUS_HOST_CAN_BE_USE:
                hosts_list.append(host.connect_ip)

        if self.group.jumper is not None:
            proxy = self.group.jumper.to_yaml()

        return {
            'gather_facts': self.gather_facts(),
            'hosts': hosts_list or 'localhost',
            'tasks': super(META, self).to_yaml(proxy)['tasks']
        }


class Mission(models.Model):
    class Meta:
        permissions = (('yo_list_mission', u'罗列任务'),
                       ('yo_create_mission', u'创建任务'),
                       ('yo_update_mission', u'更新任务'),
                       ('yo_delete_mission', u'删除任务'))
    id = models.AutoField(primary_key=True)
    uuid = models.UUIDField(auto_created=True, default=uuid.uuid4, editable=False)
    group = models.ForeignKey(Group, on_delete=models.SET_NULL, null=True, related_name='group_missions')
    metas = models.ManyToManyField(META, blank=True, related_name='missions', verbose_name=_("Mission"))
    info = models.CharField(default='', max_length=5000)
    need_validate = models.BooleanField(default=True)

    @property
    def file_list(self):
        files = []
        for meta in self.metas.all():
            if len(meta.file_list()) != 0:
                files = files + meta.file_list()
        return files

    @property
    def vars_dict(self):
        return self.group.vars_dict

    def to_yaml(self):
        tasks_list = []
        for meta in self.metas.all():
            tasks_list.append(meta.to_yaml())
        return tasks_list

    @property
    def count(self):
        return self.push_missions.count()

    # @property
    def _playbook(self):
        return yaml.dump(self.to_yaml(), default_flow_style=False)

    def model_to_dict(self):
        from django.forms.models import model_to_dict
        return model_to_dict(self)


class Push_Mission(models.Model):
    STATUS = (
        (settings.OPS_PUSH_MISSION_WAIT_EXAM, '审核工单'), # 未审核
        (settings.OPS_PUSH_MISSION_WAIT_UPLOAD, '上传文件'), # 未上传文件
        (settings.OPS_PUSH_MISSION_WAIT_RUN, '执行工单'), # 未执行
        (settings.OPS_PUSH_MISSION_RUNNING, '执行中'), # 执行中
        (settings.OPS_PUSH_MISSION_SUCCESS, '执行完毕'), # 执行完毕
        (settings.OPS_PUSH_MISSION_FAILED, '执行失败'), # 执行失败
    )

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
    results = models.TextField()
    # 关联文件
    files = models.ManyToManyField(FILE, related_name='pushmission', blank=True)

    @property
    def status(self):
        return self._status

    @status.setter
    def status(self, status):
        # 当任务状态已经小于0为异常状态的时候不改写状态值
        if self._status >= 0:
            self._status = status
            self.save()

    def results_append(self,results):
        self.results = self.results + str(results)
        self.save()


class Quick(models.Model):
    id = models.AutoField(primary_key=True)
    uuid = models.UUIDField(auto_created=True, default=uuid.uuid4, editable=False)
    data = models.CharField(default="", max_length=200)
    metatype = models.CharField(default="", max_length=200)
    user = models.ForeignKey(ExtendUser, default=None, blank=True, null=True, on_delete=models.SET_NULL)

    class Meta:
        permissions = (
            ('yo_create_quick', u'快速配置任务'),
        )
