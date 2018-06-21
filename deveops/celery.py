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
from . import celeryconfig
app.config_from_object(celeryconfig)
app.autodiscover_tasks()