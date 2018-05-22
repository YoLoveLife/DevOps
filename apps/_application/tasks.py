# -*- coding:utf-8 -*-
# !/usr/bin/env python
# Time 17-10-25
# Author Yo
# Email YoLoveLife@outlook.com

from __future__ import absolute_import, unicode_literals
from celery.task import periodic_task
from celery.schedules import crontab
from deveops.conf import REDIS_PORT,REDIS_SPACE,EXPIREDTIME
import redis

connect = redis.StrictRedis(port=REDIS_PORT,db=REDIS_SPACE)

@periodic_task(run_every=crontab(minute='*'))
def aliyunRDSInfoCatch():
    from deveops.utils import aliyun
    from deveops.conf import ALIYUN_PAGESIZE
    from deveops.utils import resolver
    from application.models import ExpiredAliyunRDS
    import datetime
    ExpiredAliyunRDS.objects.all().delete()
    countNumber = aliyun.fetch_RDSPage()
    threadNumber = int(countNumber/ALIYUN_PAGESIZE)
    now = datetime.datetime.now()
    for num in range(1,threadNumber+1):
        data = aliyun.fetch_RDSs(num)
        for dt in data:
            if not dt['DBInstanceId'][0:2] == 'rr':
                expiredTime = datetime.datetime.strptime(dt['ExpireTime'],'%Y-%m-%dT%H:%M:%SZ')
                if 0 < (expiredTime - now).days < EXPIREDTIME:
                    dt['ExpiredDay'] = (expiredTime - now).days
                    ExpiredAliyunRDS(**resolver.AliyunRDS2Json.decode(dt)).save()