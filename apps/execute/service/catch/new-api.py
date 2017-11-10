# -*- coding:utf-8 -*-
# !/usr/bin/env python
# Time 17-11-7
# Author Yo
# Email YoLoveLife@outlook.com

from execute.callback import ResultCallback
from manager.models import Host
from operation.models import PlayBook

from apps.execute.ansible.runner import AdHocRunner

__metaclass__ = type

def test_task():
    hosts = Host.objects.all()
    runner = AdHocRunner(hosts = hosts)
    runner.set_callback(ResultCallback())
    playbook = PlayBook.objects.all()[0]
    ret = runner.run(playbook.tasks.all())

if __name__ == '__main__':

    test_task()