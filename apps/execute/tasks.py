# -*- coding:utf-8 -*-
# !/usr/bin/env python
# Time 17-11-14
# Author Yo
# Email YoLoveLife@outlook.com
# from __future__ import absolute_import

# from celery.schedules import crontab
# from celery.task import periodic_task
# from celery.utils.log import get_task_logger
# from execute.utils import scrapers
# import datetime
# logger = get_task_logger(__name__)
#
#
# @periodic_task(run_every=(crontab(minute="*")))
# def scraper_example():
#     logger.info("Start task")
#     now = datetime.now()
#     result = scrapers.scraper_example(now.day, now.minute)
#     logger.info("Task finished: result = %i" % result)

# from deveops import celery_app
#
# @celery_app.task
# def ddr():
#     print('start send email to %s')
#     import time
#     time.sleep(5) #休息5秒
#     print('success')
#     return True
#
# from celery.schedules import crontab
# from celery.task import periodic_task
# @periodic_task(run_every=crontab(minute='*'))
# def some_task():
#     print('periodic task test!!!!!')
#     import time
#     time.sleep(5)
#     print('success')
#     return True

# Create your tasks here
from __future__ import absolute_import, unicode_literals
from celery.task import task

@task(name='PingOnlineTask')
def PingOnlineTask():
    from manager.models import Host
    import time
    host = Host.objects.all()[0]
    host.info = str(time.time())
    host.save()