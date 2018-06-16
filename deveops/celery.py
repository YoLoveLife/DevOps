# -*- coding:utf-8 -*-
# !/usr/bin/env python
# Time 17-10-26
# Author Yo
# Email YoLoveLife@outlook.com
from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'deveops.settings')
app = Celery('deveops')
# app.config_from_object('django.conf:settings', namespace='CELERY')

# class Config:
#     enable_utc = False
#     timezone = 'Asia/Shanghai'
#     broker_url = "redis://:@localhost:6379/3"
#     result_backend = "redis://:@localhost:6379/3"
#     task_serializer = 'pickle'
#     result_serializer = 'pickle'
#     accept_content = ['json', 'pickle']
#     # worker_log_format = '%(message)s'
#     # worker_task_log_format = '%(message)s'
#     task_eager_propagates = True
#     worker_redirect_stdouts = True
#     worker_redirect_stdouts_level = "INFO"
#     worker_hijack_root_logger = False
from . import celeryconfig
app.config_from_object(celeryconfig)
app.autodiscover_tasks()