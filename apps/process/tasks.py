# -*- coding:utf-8 -*-
# !/usr/bin/env python
# Time 17-10-25
# Author Yo
# Email YoLoveLife@outlook.com

from __future__ import absolute_import, unicode_literals
from celery import Task,task
from dns import resolver
import time
from django.conf import settings
from yocdn.models import CDN
from deveops.tools.aliyun_v2.request.cdn import AliyunCDNTool
from deveops.tools.qiniu.cdn import QiNiuCDNTool

class CDNTask(Task):
    def on_failure(self, exc, task_id, args, kwargs, einfo):
        print('{0!r} failed: {1!r}'.format(task_id, exc))


def reflush(url, nameserver):
    r = resolver.Resolver()
    r.nameservers = [nameserver]
    try:
        answers = r.query(url, 'CNAME')
        for rdata in answers:
            return rdata.to_text()[:-1]
    except resolver.NoAnswer as e:
        return ''
    except resolver.NXDOMAIN as e:
        return ''
    return ''


def pick_domain(url):
    if 'http' in url: # 如果是HTTP 或者HTTPS的话
        index = url.find('//')
        header = url.find('/', index+2)
        return url[index+2:header]
    else:
        header = url.find('/')
        return url[:header]


def choose_type(domain):
    CNAME = reflush(domain, settings.OUTER_DNS)
    if 'alikunlun' in CNAME:
        return settings.TYPE_CDN_ALIYUN
    elif 'qiniu' in CNAME:
        return settings.TYPE_CDN_QN
    elif 'wangs' in CNAME:
        return settings.TYPE_CDN_WS


def process(API, obj):
    task_id = API.tool_flush_cdn(obj.url)['RefreshTaskId']
    while True:
        dict_models = API.tool_get_task(task_id).__next__()
        CDN.objects.filter(
            uuid=obj.uuid, id=obj.id
        ).update(
            process=dict_models['process'],
            status=dict_models['status'],
        )
        if dict_models['status'] == settings.STATUS_CDN_DONE or dict_models['status'] == settings.STATUS_CDN_ERROR:
            return
        time.sleep(1)


@task(base=CDNTask)
def refresh_cdn(obj):
    type = choose_type(pick_domain(obj.url))
    CDN.objects.filter(
        uuid=obj.uuid,
        id=obj.id,
    ).update(type=type)

    if obj.type == settings.TYPE_CDN_ALIYUN:
        API = AliyunCDNTool()
        process(API, obj)
    elif obj.type == settings.TYPE_CDN_QN:
        API = QiNiuCDNTool()
        process(API, obj)
