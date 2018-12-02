# -*- coding:utf-8 -*-
# !/usr/bin/env python
# Time 17-10-25
# Author Yo
# Email YoLoveLife@outlook.com
import time
import os
import stat
from celery.task import periodic_task
from django.db.models import Q
from django.conf import settings
from manager.models import Host, Group
from manager.ansible_v2.callback import SSHCallback, DiskInodeCallback, DiskSpaceCallback, UptimeCallback
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


@periodic_task(run_every=settings.MANAGER_HOST_TIME)
def vmware2cmdb():
    from deveops.tools import vmware
    for conf in settings.VMWARE_CONF:
        API = vmware.VmwareTool(**conf)
        childrens = API.get_all_vms()
        for child in childrens:
            dict_models = API.get_vm_models(child, conf['VMWARE_SERVER'])
            host_query = Host.objects.filter(vmware_id=dict_models['vmware_id'], connect_ip=dict_models['connect_ip'])
            if not host_query.exists():
                host_maker(dict_models)


@periodic_task(run_every=settings.MANAGER_HOST_TIME)
def aliyun2cmdb():
    from deveops.tools.aliyun_v2.request import ecs
    API = ecs.AliyunECSTool()
    for dict_models in API.tool_get_instances_models():
        host_query = Host.objects.filter(aliyun_id=dict_models['aliyun_id'], connect_ip=dict_models['connect_ip'])
        if not host_query.exists():
            host_maker(dict_models)
        else:
            host_updater(host_query, dict_models)


@periodic_task(run_every=settings.MANAGER_HOST_TIME)
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


"""
资产巡检
"""


@periodic_task(run_every=settings.MANAGER_HOST_SSH_CHECK)
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
    vars_dict = group.vars_dict

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
    from manager.ansible_v2.playsource import PING_PLAY_SOURCE

    PING_PLAY_SOURCE[0]['hosts'] = list(group.hosts.exclude(
        Q(_status=settings.STATUS_HOST_PAUSE) or Q(_status=settings.STATUS_HOST_CLOSE)
    ).values_list('connect_ip', flat=True))

    ssh_playbook.import_task(PING_PLAY_SOURCE)
    ssh_playbook.run()


@periodic_task(run_every=settings.MANAGER_HOST_DISK_CHECK)
def disk_space():
    from manager.ansible_v2.playsource import DISK_SPACE_PLAY_SOURCE
    for group in Group.objects.all():
        if group.key is not None and group.jumper is not None:
            callback = DiskSpaceCallback(group)
            run_disk_overflow(group, DISK_SPACE_PLAY_SOURCE, callback)


@periodic_task(run_every=settings.MANAGER_HOST_DISK_CHECK)
def disk_inode():
    from manager.ansible_v2.playsource import DISK_INODE_PLAY_SOURCE
    for group in Group.objects.all():
        if group.key is not None and group.jumper is not None:
            callback = DiskInodeCallback(group)
            run_disk_overflow(group, DISK_INODE_PLAY_SOURCE, callback)


def run_disk_overflow(group, RESOURCE, callback):
    # 准备变量
    vars_dict = group.vars_dict

    # 创建临时目录
    TMP = settings.OPS_ROOT + '/' + str(time.time()) + '/'
    if not os.path.exists(TMP):
        os.makedirs(TMP)

    KEY = TMP + str(time.time()) + '.key'
    write_key(group.key, KEY)

    dof = Playbook(group, KEY, callback)
    dof.import_vars(vars_dict)

    RESOURCE[0]['hosts'] = list(group.hosts.filter(
        Q(_status=settings.STATUS_HOST_CAN_BE_USE) or
        Q(_status=settings.STATUS_HOST_DISK_SPACE_FULL) or
        Q(_status=settings.STATUS_HOST_DISK_INODE_FULL)
    ).values_list('connect_ip', flat=True))

    dof.import_task(RESOURCE)
    dof.run()


@periodic_task(run_every=settings.MANAGER_HOST_LOAD_CHECK)
def uptime():
    for group in Group.objects.all():
        if group.key is not None and group.jumper is not None:
            run_uptime(group)
            # break


def run_uptime(group):
    # 准备变量
    vars_dict = group.vars_dict

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
    from manager.ansible_v2.playsource import UPTIME_PLAY_SOURCE

    UPTIME_PLAY_SOURCE[0]['hosts'] = list(group.hosts.filter(
        Q(_status=settings.STATUS_HOST_CAN_BE_USE) or Q(_status=settings.STATUS_HOST_UPTIME_ERROR)
    ).values_list('connect_ip', flat=True))

    uptime_playbook.import_task(UPTIME_PLAY_SOURCE)
    uptime_playbook.run()
