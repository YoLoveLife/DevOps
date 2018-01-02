# -*- coding:utf-8 -*-
# !/usr/bin/env python
# Time 17-10-26
# Author Yo
# Email YoLoveLife@outlook.com

# from __future__ import absolute_import,unicode_literals
# import os
# from celery import Celery,platforms
# from execute.service import base as BaseTask
# os.environ.setdefault('DJANGO_SETTINGS_MODULE','deveops.settings')
# platforms.C_FORCE_ROOT = True
#
# app = Celery('deveops')
# app.config_from_object('django.conf:settings')
# from django.conf import settings
# app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)

# from celery.schedules import crontab
# from celery.task import periodic_task

# @periodic_task(
#     run_every=(crontab(minute='*',hour='*')),
#     name="PingOnlineTask",
#     ignore_result=True
# )
# def PingOnlineTask():
#     # BaseTask.PingOnlineService()
#     # from manager.models import Host
#     # import time
#     # host = Host.objects.all()[0]
#     # host.info = str(time.time())
#     # host.save()
#     from manager.models import Host
#     from execute.ansible.runner import YoRunner
#     from execute.callback import ResultCallback
#     from operation.models import PlayBook
#     from django.conf import settings
#
#     hosts = Host.objects.all()
#     import time
#     for host in hosts:
#         host.info = str(time.time())
#         host.save()
#     runner = YoRunner(hosts=hosts, extra_vars={})
#     runner.set_callback(ResultCallback())
#     playbook = PlayBook.objects.filter(id=settings.PING_PLAYBOOK_TASK_ID)[0]
#     ret = runner.run(playbook.tasks.all())


from __future__ import absolute_import, unicode_literals
import os
from celery import Celery

# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'proj.settings')

app = Celery('proj')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings')
from django.conf import settings
# Load task modules from all registered Django app configs.
from django.apps import apps
# app.autodiscover_tasks(lambda: [n.name for n in apps.get_app_configs()])
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)

from celery.task import periodic_task
from celery.schedules import crontab
@periodic_task(
    run_every=(crontab(minute='*')),
    name="execute.tasks.PingOnlineTask",
    ignore_result=True
)
def PingOnlineTask():
    from manager.models import Host
    import time
    host = Host.objects.all()[0]
    host.info = str(time.time())
    host.save()

# @app.task(bind=True)
# def debug_task(self):
#     print('Request: {0!r}'.format(self.request))
from celery.schedules import crontab
#
# app.conf.update(
#     CELERYBEAT_SCHEDULE = {
#         # Executes every Monday morning at 7:30 A.M
#         'add-every-monday-morning': {
#             'task': 'execute.tasks.PingOnlineTask',
#             'schedule': crontab(hour=7, minute=30, day_of_week=1),
#             'args': (16, 16),
#         },
#     }
# )