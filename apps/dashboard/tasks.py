# -*- coding:utf-8 -*-
# !/usr/bin/env python
# Time 17-10-25
# Author Yo
# Email YoLoveLife@outlook.com

from __future__ import absolute_import, unicode_literals
from celery.task import periodic_task
from celery.schedules import crontab
from deveops.conf import ALIYUN_PAGESIZE,REDIS_PORT,REDIS_SPACE,EXPIREDTIME
import redis
import datetime
import json
from deveops.utils import aliyun
from deveops.utils import resolver

connect = redis.StrictRedis(port=REDIS_PORT,db=REDIS_SPACE)

@periodic_task(run_every=crontab(minute='*'))
def aliyunECSExpiredInfoCatch():
    from dashboard.models import ExpiredAliyunECS

    ExpiredAliyunECS.objects.all().delete()
    countNumber = aliyun.fetch_ECSPage()
    threadNumber = int(countNumber/ALIYUN_PAGESIZE)
    now = datetime.datetime.now()
    for num in range(1,threadNumber+1):
        data = aliyun.fetch_Instances(num)
        for dt in data:
            expiredTime = datetime.datetime.strptime(dt['ExpiredTime'],'%Y-%m-%dT%H:%MZ')
            if 0 < (expiredTime-now).days < EXPIREDTIME:
                dt['ExpiredDay'] = (expiredTime-now).days
                instance_data = resolver.AliyunECS2Json.decode(dt)
                instance_data.pop('os')
                ExpiredAliyunECS(**instance_data).save()


@periodic_task(run_every=crontab(minute='*'))
def aliyunRDSInfoCatch():
    from dashboard.models import ExpiredAliyunRDS

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


@periodic_task(run_every=crontab(minute='*'))
def managerStatusCatch():
    connect.delete('MANAGER_STATUS')

    status = {}
    # 資產計數
    from manager import models as Manager
    status['host_count'] = Manager.Host.objects.count()
    status['group_count'] = Manager.Group.objects.count()

    # 類型統計
    systypes = Manager.System_Type.objects.all()
    sys_list = []
    for sys in systypes:
        sys_list.append({'name': sys.name,'value': sys.hosts_detail.count()})
    status['systemtype'] = sys_list
    # 不同系统类型所涉及的主机个数

    positions = Manager.Position.objects.all()
    pos_list = []
    for pos in positions:
        pos_list.append({'name': pos.name,'value': pos.hosts_detail.count()})
    status['position'] = pos_list
    # 不同位置所涉及的主机个数

    groups = Manager.Group.objects.all()
    group_list = []
    for group in groups:
        group_list.append({'name': group.name,'value': group.hosts.count()})
    status['groups'] = group_list

    status_json = json.dumps(status)
    connect.set('MANAGER_STATUS',status_json)

