# -*- coding:utf-8 -*-
# !/usr/bin/env python
# Time 17-10-25
# Author Yo
# Email YoLoveLife@outlook.com
import os
import django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "deveops.settings")
django.setup()

import redis
import time, os, stat
from celery.task import periodic_task
from celery.schedules import crontab
from django.conf import settings
from django.db.models import Q
from manager.models import Host, Group
from manager.ansible_v2.callback import SSHCallback, DiskOverFlowCallback, UptimeCallback
from deveops.ansible_v2.playbook import Playbook

def host_maker(dict_models):
    Host.objects.create(**dict_models)


def host_updater(obj, dict_models):
    status = dict_models.pop('status')
    if obj.get().status == settings.STATUS_HOST_PAUSE:
        if status == settings.STATUS_HOST_CAN_BE_USE:
            pass
        else:
            dict_models['_status'] = settings.STATUS_HOST_CLOSE
    else:
        dict_models['_status'] = status

    obj.update(**dict_models)


@periodic_task(run_every=settings.MANAGER_TIME)
def vmware2cmdb():
    from deveops.tools import vmware
    API = vmware.VmwareTool()
    childrens = API.get_all_vms()
    for child in childrens:
        dict_models = API.get_vm_models(child)
        host_query = Host.objects.filter(vmware_id=dict_models['vmware_id'], connect_ip=dict_models['connect_ip'])
        if not host_query.exists():
            host_maker(dict_models)


@periodic_task(run_every=settings.MANAGER_TIME)
def aliyun2cmdb():
    from deveops.tools.aliyun_v2.request import ecs
    API = ecs.AliyunECSTool()
    for dict_models in API.tool_get_instances_models():
        host_query = Host.objects.filter(aliyun_id=dict_models['aliyun_id'], connect_ip=dict_models['connect_ip'])
        if not host_query.exists():
            host_maker(dict_models)
        else:
            host_updater(host_query, dict_models)


@periodic_task(run_every=settings.MANAGER_TIME)
def cmdb2aliyun():
    from deveops.tools.aliyun_v2.request import ecs
    from django.db.models import Q
    API = ecs.AliyunECSTool()
    queryset = Host.objects.filter(~Q(aliyun_id=''))
    for host in queryset:
        status = API.tool_get_instance_models(host.aliyun_id).__next__()
        if status == 'delete':
            host.delete()
        else:
            expired_models = API.tool_get_instance_expired_models(host.aliyun_id).__next__()
            if expired_models.get('expired') < settings.ALIYUN_OVERDUETIME:
                host.delete()
            else:
                if host.status == settings.STATUS_HOST_PAUSE:
                    if status == settings.STATUS_HOST_CAN_BE_USE:
                        pass
                    else:
                        host.status = settings.STATUS_HOST_CLOSE
                else:
                    host.status = status

connect = redis.StrictRedis(host=settings.REDIS_HOST,port=settings.REDIS_PORT,db=settings.REDIS_SPACE,password=settings.REDIS_PASSWD)


@periodic_task(run_every=crontab(minute='*/5'))
def statistics_group():
    connect.delete('GROUP_STATUS')

    groups = Group.objects.all()
    group_name = []
    group_value = []
    for group in groups:
        group_name.append(group.name)
        group_value.append(group.hosts.count())
    connect.set('GROUP_STATUS', {'name':group_name,'value':group_value})


@periodic_task(run_every=crontab(minute='*/5'))
def statistics_manager():
    host_count = Host.objects.count()
    group_count = Group.objects.count()

    connect.set('HOST_COUNT', host_count)
    connect.set('GROUP_COUNT', group_count)



"""
    资产巡检
"""


@periodic_task(run_every=settings.CHECK_TIME)
def ssh_check():
    for group in Group.objects.all():
        if group.key is not None and group.jumper is not None:
            run_ssh_check(group)
            # break


def write_key(key, file_path):
    try:
        f = open(file_path, 'w')
        f.write(key.private_key)
        f.close()
    except Exception:
        return '~/.ssh/id_rsa'
    os.chmod(file_path, stat.S_IWUSR | stat.S_IRUSR)

    return file_path


def run_ssh_check(group):
    # 准备变量
    vars_dict = {}

    for var in group.group_vars.all():
        vars_dict[var.key] = var.value

    if group.jumper is not None and group.key is not None:
        vars_dict['JUMPER_IP'] = group.jumper.connect_ip
        vars_dict['JUMPER_PORT'] = group.jumper.sshport

    # 创建临时目录
    TMP = settings.OPS_ROOT + '/' + str(time.time()) + '/'
    if not os.path.exists(TMP):
        os.makedirs(TMP)

    KEY = TMP + str(time.time()) + '.key'
    write_key(group.key, KEY)

    # Playbook实例
    callback = SSHCallback(group)
    ssh_playbook = Playbook(group, KEY, callback)
    ssh_playbook.import_vars(vars_dict)
    from manager.ansible_v2.play_source import PING_PLAY_SOURCE

    PING_PLAY_SOURCE[0]['hosts'] = list(group.hosts.exclude(
        Q(_status=settings.STATUS_HOST_PAUSE) or Q(_status=settings.STATUS_HOST_CLOSE)
    ).values_list('connect_ip', flat=True))

    ssh_playbook.import_task(PING_PLAY_SOURCE)
    ssh_playbook.run()


@periodic_task(run_every=settings.CHECK_TIME)
def disk_overflow():
    for group in Group.objects.all():
        if group.key is not None and group.jumper is not None:
            run_disk_overflow(group)
            # break


def run_disk_overflow(group):
    # 准备变量
    vars_dict = {}

    for var in group.group_vars.all():
        vars_dict[var.key] = var.value

    if group.jumper is not None and group.key is not None:
        vars_dict['JUMPER_IP'] = group.jumper.connect_ip
        vars_dict['JUMPER_PORT'] = group.jumper.sshport

    # 创建临时目录
    TMP = settings.OPS_ROOT + '/' + str(time.time()) + '/'
    if not os.path.exists(TMP):
        os.makedirs(TMP)

    KEY = TMP + str(time.time()) + '.key'
    write_key(group.key, KEY)

    # Playbook实例
    callback = DiskOverFlowCallback(group)
    dof = Playbook(group, KEY, callback)
    dof.import_vars(vars_dict)
    from manager.ansible_v2.play_source import DISK_PLAY_SOURCE

    DISK_PLAY_SOURCE[0]['hosts'] = list(group.hosts.filter(
        _status=settings.STATUS_HOST_CAN_BE_USE
    ).values_list('connect_ip', flat=True))

    dof.import_task(DISK_PLAY_SOURCE)
    dof.run()


@periodic_task(run_every=settings.CHECK_TIME)
def uptime():
    for group in Group.objects.all():
        if group.key is not None and group.jumper is not None:
            run_uptime(group)
            # break


def run_uptime(group):
    # 准备变量
    vars_dict = {}

    for var in group.group_vars.all():
        vars_dict[var.key] = var.value

    if group.jumper is not None and group.key is not None:
        vars_dict['JUMPER_IP'] = group.jumper.connect_ip
        vars_dict['JUMPER_PORT'] = group.jumper.sshport

    # 创建临时目录
    TMP = settings.OPS_ROOT + '/' + str(time.time()) + '/'
    if not os.path.exists(TMP):
        os.makedirs(TMP)

    KEY = TMP + str(time.time()) + '.key'
    write_key(group.key, KEY)

    # Playbook实例
    callback = UptimeCallback(group)
    uptime_playbook = Playbook(group, KEY, callback)
    uptime_playbook.import_vars(vars_dict)
    from manager.ansible_v2.play_source import UPTIME_PLAY_SOURCE

    UPTIME_PLAY_SOURCE[0]['hosts'] = list(group.hosts.filter(
        _status=settings.STATUS_HOST_CAN_BE_USE
    ).values_list('connect_ip', flat=True))

    uptime_playbook.import_task(UPTIME_PLAY_SOURCE)
    uptime_playbook.run()
