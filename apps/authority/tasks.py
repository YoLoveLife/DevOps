# -*- coding:utf-8 -*-
# !/usr/bin/env python
# Time 17-10-25
# Author Yo
# Email YoLoveLife@outlook.com
import socket
import paramiko
import os
import stat
import time
from django.conf import settings
from celery import Task, task


class JumperTask(Task):
    def on_failure(self, exc, task_id, args, kwargs, einfo):
        print('{0!r} failed: {1!r}'.format(task_id, exc))


def write_key(key, file_path):
    try:
        f = open(file_path, 'w')
        f.write(key.private_key)
        f.close()
    except Exception as e:
        return '~/.ssh/id_rsa'
    os.chmod(file_path, stat.S_IWUSR | stat.S_IRUSR)

    return file_path


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
    try:
        if obj.group is None or obj.group.key is None:
            obj._status = settings.STATUS_JUMPER_NO_KEY
            obj.save()
            return
    except Exception as e:
        obj._status = settings.STATUS_JUMPER_NO_KEY
        obj.save()
        return

    # 创建临时目录
    TMP = settings.OPS_ROOT + '/' + str(time.time()) + '/'
    if not os.path.exists(TMP):
        os.makedirs(TMP)

    KEY = TMP + str(time.time()) + '.key'
    write_key(obj.group.key, KEY)

    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.MissingHostKeyPolicy)
    try:
        ssh.connect(hostname=obj.connect_ip, port=obj.sshport, username='root', key_filename=KEY)
    except paramiko.AuthenticationException as e:
        obj._status = settings.STATUS_JUMPER_WRONG_KEY
        obj.save()
        return

    obj._status = settings.STATUS_JUMPER_CAN_BE_USE
    obj.save()
