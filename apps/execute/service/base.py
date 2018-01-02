# -*- coding:utf-8 -*-
# !/usr/bin/env python
# Time 17-11-13
# Author Yo
# Email YoLoveLife@outlook.com
from manager.models import Host
from execute.ansible.runner import YoRunner
from execute.callback import ResultCallback
from operation.models import PlayBook
from django.conf import settings

def PingOnlineService():
    hosts = Host.objects.all()
    import time
    for host in hosts:
        host.info = str(time.time())
        host.save()
    runner = YoRunner(hosts=hosts, extra_vars={})
    runner.set_callback(ResultCallback())
    playbook = PlayBook.objects.filter(id=settings.PING_PLAYBOOK_TASK_ID)[0]
    ret = runner.run(playbook.tasks.all())