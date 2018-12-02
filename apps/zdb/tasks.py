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
from celery import Task,task
class ZDBTask(Task):
    def on_failure(self, exc, task_id, args, kwargs, einfo):
        print('{0!r} failed: {1!r}'.format(task_id, exc))


@task(base=ZDBTask)
def status_flush(instance):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(settings.SSH_TIMEOUT)
    try:
        s.connect((str(instance.connect_ip), int(instance.port)))
        print(instance.connect_ip, instance.port)
    except socket.timeout as e:
        print('timeout')
        instance._status = settings.STATUS_DB_INSTANCE_UNREACHABLE
        instance.save()
        return
    except ConnectionRefusedError as e:
        print('refuse')
        instance._status = settings.STATUS_DB_INSTANCE_CONNECT_REFUSE
        instance.save()
        return
    except Exception as e:
        print('exception')
        instance._status = settings.STATUS_DB_INSTANCE_UNREACHABLE
        instance.save()
        return

    try:
        print(instance.connect_ip, instance.port, instance.admin_user, instance.password)
        db = MySQLdb.connect(
            host=instance.connect_ip,
            port=instance.port,
            user=instance.admin_user,
            password=instance.password
        )
    except MySQLdb.connections.OperationalError as e:
        print('password wrong',e)
        instance._status = settings.STATUS_DB_INSTANCE_PASSWORD_WRONG
        instance.save()
        return

    instance._status = settings.STATUS_DB_INSTANCE_CAN_BE_USE
    instance.save()


@task(base=ZDBTask)
def instance_create(instance, detail):
    import string, random
    all_choice = string.ascii_letters + string.digits + string.punctuation
    passwd = ''
    for i in range(16):
        passwd += random.choice(all_choice)

    print(passwd)
    print(instance, detail)

    hosts_list = detail['group'].users_list_byconnectip
