# -*- coding:utf-8 -*-
# !/usr/bin/env python
# Time 09 13:49
# Author Yo
# Email YoLoveLife@outlook.com
from __future__ import absolute_import,unicode_literals
from .celery import app as celery_app

__all__ = ['celery_app']