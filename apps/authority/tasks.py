# -*- coding:utf-8 -*-
# !/usr/bin/env python
# Time 17-10-25
# Author Yo
# Email YoLoveLife@outlook.com
from __future__ import absolute_import, unicode_literals
from celery import Task,task
import socket
from django.conf import settings
class JumperTask(Task):
    def on_failure(self, exc, task_id, args, kwargs, einfo):
        print('{0!r} failed: {1!r}'.format(task_id, exc))


@task(base=JumperTask)
def jumper_status_flush(obj):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(settings.SSH_TIMEOUT)
    try:
        s.connect((str(obj.connect_ip), int(obj.sshport)))
    except socket.timeout as e:
        obj._status = settings.STATUS_JUMPER_UNREACHABLE
        obj.save()
        return
    except ConnectionRefusedError as e:
        obj._status = settings.STATUS_JUMPER_UNREACHABLE
        obj.save()
        return
    except Exception as e:
        obj._status = settings.STATUS_JUMPER_UNREACHABLE
        obj.save()
        return
    obj._status = settings.STATUS_JUMPER_CAN_BE_USE
    obj.save()