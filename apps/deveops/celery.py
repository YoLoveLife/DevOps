# -*- coding:utf-8 -*-
# !/usr/bin/env python
# Time 17-10-26
# Author Yo
# Email YoLoveLife@outlook.com

from __future__ import absolute_import,unicode_literals
import os
from celery import Celery,platforms
from execute.service import base as BaseTask
os.environ.setdefault('DJANGO_SETTINGS_MODULE','deveops.settings')
platforms.C_FORCE_ROOT = True
app = Celery('deveops')
app.config_from_object('django.conf:settings')
from django.conf import settings
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)

from celery.schedules import crontab
from celery.task import periodic_task

@periodic_task(
    run_every=(crontab(minute='*',hour='*')),
    name="PingOnlineTask",
    ignore_result=True
)
def PingOnlineTask():
    BaseTask.PingOnlineService()
