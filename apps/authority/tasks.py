# -*- coding:utf-8 -*-
# !/usr/bin/env python
# Time 17-10-25
# Author Yo
# Email YoLoveLife@outlook.com

from __future__ import absolute_import, unicode_literals
from celery.task import periodic_task
from celery.schedules import crontab
from authority.models import Jumper
from django.core.exceptions import ObjectDoesNotExist
@periodic_task(run_every=crontab(minute='*'))
def jumperStatusCheck():
    host = None
    for jumper in Jumper.objects.all():
        if not jumper.check_status():
            # 不是可达的话
            try:
                for host in jumper.group.hosts.all():
                    if host.status == 1:
                        host.status = 2
                        host.save()
            except ObjectDoesNotExist:
                pass
        else:
            # 如果是可达的话
            try:
                for host in jumper.group.hosts.all():
                    if host.status != 0:
                        host.status = 1
                        host.save()
            except ObjectDoesNotExist:
                pass
        jumper.save()