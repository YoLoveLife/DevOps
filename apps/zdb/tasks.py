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
    except socket.timeout:
        instance._status = settings.STATUS_DB_INSTANCE_UNREACHABLE
        instance.save()
    except Exception as e:
        instance._status = settings.STATUS_DB_INSTANCE_UNREACHABLE
        instance.save()
    instance._status = settings.STATUS_DB_INSTANCE_CAN_BE_USE
    instance.save()


