# -*- coding:utf-8 -*-
# !/usr/bin/env python
# Time 17-10-25
# Author Yo
# Email YoLoveLife@outlook.com
#
# from celery.schedules import crontab
# from celery.task import periodic_task
# from celery import shared_task
# @periodic_task(
#     run_every=(crontab(minute='*/2')),
#     name="ddr",
#     ignore_result=True
# )
# def ddr():
#     from manager.models import Host
#     import time
#     host = Host.objects.all()[0]
#     host.info = str(time.time())
#     host.save()