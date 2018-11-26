# -*- coding:utf-8 -*-
# !/usr/bin/env python
# Time 18-3-29
# Author Yo
# Email YoLoveLife@outlook.com
from deveops.ansible_v2.callback import Callback
from django.conf import settings

__all__ = [
    'SSHCallback', 'DiskInodeCallback', 'DiskSpaceCallback',
    'UptimeCallback',
]

INDENT = 4


class SSHCallback(Callback):
    def __init__(self, group):
        self.group = group
        super(SSHCallback, self).__init__()

    def v2_runner_on_ok(self, result, **kwargs):
        connect_ip = result._host.address
        host = self.group.hosts.filter(connect_ip=connect_ip).get()
        if host._status == settings.STATUS_HOST_DENY_OR_REFUSE:
            host._status = settings.STATUS_HOST_CAN_BE_USE
            host.save()
        return super(SSHCallback, self).v2_runner_on_ok(result, **kwargs)

    def v2_runner_on_unreachable(self, result):
        connect_ip = result._host.address
        host = self.group.hosts.filter(connect_ip=connect_ip).get()
        if host._status != settings.STATUS_HOST_CLOSE or host._status != settings.STATUS_HOST_PAUSE:
            host._status = settings.STATUS_HOST_DENY_OR_REFUSE
            host.save()
        return super(SSHCallback, self).v2_runner_on_unreachable(result)


class DiskSpaceCallback(Callback):
    def __init__(self, group):
        self.group = group
        super(DiskSpaceCallback, self).__init__()

    def v2_runner_on_ok(self, result, **kwargs):
        if result._task.action != 'set_fact':
            percentage = result._result['stdout']
            connect_ip = result._host.address
            print('Disk_Space',percentage,connect_ip)
            host = self.group.hosts.filter(connect_ip=connect_ip).get()
            if int(percentage[:-1]) > settings.SPACE_DISK_LIMIT:  # 磁盘溢出
                print('溢出')
                if host._status == settings.STATUS_HOST_CAN_BE_USE and host:
                    print('改变主机状态')
                    host._status = settings.STATUS_HOST_DISK_SPACE_FULL
                    host.save()
            else:  # 磁盘不溢出
                print('不溢出')
                if host._status == settings.STATUS_HOST_DISK_SPACE_FULL:
                    host._status = settings.STATUS_HOST_CAN_BE_USE
                    host.save()
        super(DiskSpaceCallback, self).v2_runner_on_ok(result, **kwargs)


class DiskInodeCallback(Callback):
    def __init__(self, group):
        self.group = group
        super(DiskInodeCallback, self).__init__()

    def v2_runner_on_ok(self, result, **kwargs):
        if result._task.action != 'set_fact':
            percentage = result._result['stdout']
            connect_ip = result._host.address
            print('Disk_Inode',percentage,connect_ip)
            host = self.group.hosts.filter(connect_ip=connect_ip).get()
            if int(percentage[:-1]) > settings.INODE_DISK_LIMIT:  # 磁盘溢出
                print('溢出')
                if host._status == settings.STATUS_HOST_CAN_BE_USE and host:
                    print('改变主机状态')
                    host._status = settings.STATUS_HOST_DISK_INODE_FULL
                    host.save()
            else:  # 磁盘不溢出
                print('不溢出')
                if host._status == settings.STATUS_HOST_DISK_INODE_FULL:
                    host._status = settings.STATUS_HOST_CAN_BE_USE
                    host.save()
        super(DiskInodeCallback, self).v2_runner_on_ok(result, **kwargs)


class UptimeCallback(Callback):
    def __init__(self, group):
        self.group = group
        self.core = {}
        super(UptimeCallback, self).__init__()

    def v2_runner_on_ok(self, result, **kwargs):
        connect_ip = result._host.address
        if result._task.action == 'set_fact' or result._task.action=='setup':
            pass
        elif 'cpus' in result._result['stdout']:
            self.core[connect_ip] = result._result['stdout'].split('cpus')[1]
        else:
            loads = result._result['stdout'].split('load average:')[1]
            host = self.group.hosts.filter(connect_ip=connect_ip).get()
            for load in loads.split(',')[:-1]:
                if float(load.strip()) > float(self.core[connect_ip]) * (settings.UPTIME_LIMIT/100) and host._status == settings.STATUS_HOST_CAN_BE_USE:
                    host._status = settings.STATUS_HOST_UPTIME_ERROR
                    host.save()
                    return super(UptimeCallback, self).v2_runner_on_ok(result, **kwargs)
            if host._status == settings.STATUS_HOST_UPTIME_ERROR:
                host._status = settings.STATUS_HOST_CAN_BE_USE
                host.save()
        return super(UptimeCallback, self).v2_runner_on_ok(result, **kwargs)

