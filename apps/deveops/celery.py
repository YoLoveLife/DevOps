# -*- coding:utf-8 -*-
# !/usr/bin/env python
# Time 17-10-26
# Author Yo
# Email YoLoveLife@outlook.com

from __future__ import absolute_import,unicode_literals
import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE','deveops.settings')

app = Celery('deveops',
             broker='redis://localhost:6379//'
             )
# app.config_from_object('django.conf:settings',namespace='CELERY')

app.autodiscover_tasks()

@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))

