# -*- coding:utf-8 -*-
# !/usr/bin/env python
# Time 17-10-25
# Author Yo
# Email YoLoveLife@outlook.com

from __future__ import absolute_import, unicode_literals
from celery.task import periodic_task
from celery.schedules import crontab
from django.db.models import Q
import celery
import MySQLdb
from django.conf import settings
import socket
import os,stat,time
from ezsetup.ansible.callback import EZSetupCallback
from ezsetup.ansible.playbook import EZSetupPlaybook
from celery import Task,task
class EZSetupTask(Task):
    def on_failure(self, exc, task_id, args, kwargs, einfo):
        print('{0!r} failed: {1!r}'.format(task_id, exc))

def write_key(key, file_path):
    try:
        print('write_key')
        f = open(file_path, 'w')
        f.write(key.private_key)
        f.close()
    except Exception:
        return '~/.ssh/id_rsa'
    os.chmod(file_path, stat.S_IWUSR | stat.S_IRUSR)

    return file_path


@task(base=EZSetupTask)
def install_redis(instance, detail):
    host_list = instance.group.users_list_byconnectip
    vars_dict = {}
    for var in instance.group.group_vars.all():
        vars_dict[var.key] = var.value

    vars_dict['JUMPER'] = instance.group.jumper.connect_ip
    #vars_dict['HOSTS'] = ':'.join(list(instance.hosts.filter(_status=settings.STATUS_HOST_CAN_BE_USE).values_list('connect_ip', flat=True)))
    vars_dict['ROLE'] = 'ddr'

    # 创建临时目录
    TMP = settings.OPS_ROOT + '/' + str(instance.uuid) + '/'
    if not os.path.exists(TMP):
        os.makedirs(TMP)

    KEY = TMP + str(time.time()) + '.key'
    write_key(instance.group.key, KEY)

    callback = EZSetupCallback(instance)
    ezsetup = EZSetupPlaybook(host_list, KEY, callback, instance)
    ezsetup.import_vars(vars_dict)
    from ezsetup.ansible.play_source import PLAY_SOURCE
    PLAY_SOURCE['hosts'] = list(instance.hosts.filter(_status=settings.STATUS_HOST_CAN_BE_USE).values_list('connect_ip', flat=True))
    ezsetup.import_task(PLAY_SOURCE)
    instance.status = settings.STATUS_EZSETUP_INSTALLING
    # ezsetup.run()





@task(base=EZSetupTask)
def install_mysql(instance, detail):
    print('456')
    pass