# -*- coding:utf-8 -*-
# !/usr/bin/env python
# Time 18-3-29
# Author Yo
# Email YoLoveLife@outlook.com
from django.conf import settings
from deveops.ansible_v2.callback import Callback
from manager.models import Host
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




class DiskOverFlowCallback(Callback):
    def __init__(self, group):
        self.group = group
        super(DiskOverFlowCallback, self).__init__()

    def v2_runner_on_ok(self, result, **kwargs):
        if result._task.action != 'set_fact':
            percentage = result._result['stdout']
            connect_ip = result._host.address
            host = self.group.hosts.filter(connect_ip=connect_ip).get()
            if int(percentage[:-1]) > settings.DISK_LIMIT:  # 磁盘溢出
                if host._status == settings.STATUS_HOST_CAN_BE_USE:
                    host._status = settings.STATUS_HOST_DISK_FULL
                    host.save()
            else:  # 磁盘不溢出
                if host._status == settings.STATUS_HOST_DISK_FULL:
                    host._status = settings.STATUS_HOST_CAN_BE_USE
                    host.save()
        super(DiskOverFlowCallback, self).v2_runner_on_ok(result, **kwargs)


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
                # print(connect_ip, float(load.strip()), float(self.core[connect_ip]) * (settings.UPTIME_LIMIT/100))
                if float(load.strip()) > float(self.core[connect_ip]) * (settings.UPTIME_LIMIT/100) and host._status == settings.STATUS_HOST_CAN_BE_USE:
                    host._status = settings.STATUS_HOST_UPTIME_ERROR
                    host.save()
                    return super(UptimeCallback, self).v2_runner_on_ok(result, **kwargs)
            if host._status == settings.STATUS_HOST_UPTIME_ERROR:
                host._status = settings.STATUS_HOST_CAN_BE_USE
                host.save()
        return super(UptimeCallback, self).v2_runner_on_ok(result, **kwargs)

