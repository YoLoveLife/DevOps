# -*- coding:utf-8 -*-
# !/usr/bin/env python
# Time 17-10-25
# Author Yo
# Email YoLoveLife@outlook.com

from __future__ import absolute_import, unicode_literals
from celery import Task,task
from django.conf import settings
from deveops.tools.qiniu.cdn import QiNiuCDNTool
from deveops.tools.aliyun.cdn import AliyunCDNTool
from deveops.tools.wangsu.cdn import WangsuCDNTool

class CDNTask(Task):
    def on_failure(self, exc, task_id, args, kwargs, einfo):
        print('{0!r} failed: {1!r}'.format(task_id, exc))


@task(base=CDNTask)
def clean_cdn(obj):
    if obj.type == settings.TYPE_CDN_ALIYUN:
        API = AliyunCDNTool()
        status = API.request_to_result(API.request_to_cdn(obj.url))
        if status:
            obj.status = settings.STATUS_CDN_DONE
        else:
            obj.status = settings.STATUS_CDN_ERROR

    elif obj.type == settings.TYPE_CDN_QN:
        API = QiNiuCDNTool()
        status = API.refresh(obj.url)
        if status:
            obj.status = settings.STATUS_CDN_DONE
        else:
            obj.status = settings.STATUS_CDN_ERROR

    elif obj.type == settings.TYPE_CDN_WS:
        API = WangsuCDNTool()
        pass
        if True:
            obj.status = settings.STATUS_CDN_DONE
        else:
            obj.status = settings.STATUS_CDN_ERROR

    obj.save()