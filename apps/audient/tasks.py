# -*- coding:utf-8 -*-
# !/usr/bin/env python
# Time 17-10-25
# Author Yo
# Email YoLoveLife@outlook.com
from __future__ import absolute_import
from celery.task import periodic_task
from celery.schedules import crontab


@periodic_task(run_every=crontab(minute='*'))
def email_audient():
    pass


@periodic_task(run_every=crontab(minute='*'))
def phone_audient():
    pass
