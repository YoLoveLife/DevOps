# -*- coding:utf-8 -*-
# !/usr/bin/env python
# Time 17-10-25
# Author Yo
# Email YoLoveLife@outlook.com

from celery.task import periodic_task
from celery.schedules import crontab
from manager.models import Host,HostDetail,Position,System_Type
from deveops.conf import REDIS_PORT,REDIS_SPACE,EXPIREDTIME
import redis

connect = redis.StrictRedis(port=REDIS_PORT,db=REDIS_SPACE)

from celery import shared_task

@periodic_task(run_every=crontab(minute=50,hour=0))
def aliyunECSInfoCatch():
    from deveops.utils import aliyun
    from deveops.conf import ALIYUN_PAGESIZE
    from deveops.utils import resolver
    from manager.models import Host
    import datetime
    countNumber = aliyun.fetch_ECSPage()
    now = datetime.datetime.now()
    position = None
    systype = None
    if Position.objects.filter(name__contains='阿里云').exists():
        position = Position.objects.filter(name__contains='阿里云').get()
    else:
        position = Position.objects.create(name='阿里云')

    threadNumber = int(countNumber/ALIYUN_PAGESIZE)
    for num in range(1,threadNumber+1):
        data = aliyun.fetch_Instances(num)
        for dt in data:
            expiredTime = datetime.datetime.strptime(dt['ExpiredTime'],'%Y-%m-%dT%H:%MZ')
            dt['ExpiredDay'] = (expiredTime-now).days
            data_dist = resolver.AliyunECS2Json.decode(dt)
            if not data_dist.__contains__('connect_ip'):
                continue
            query = Host.objects.filter(detail__aliyun_id=data_dist['recognition_id'])
            status = 0
            if System_Type.objects.filter(name__contains=data_dist['os']).exists():
                systype = System_Type.objects.filter(name__contains=data_dist['os']).get()
            else:
                systype = System_Type.objects.create(name=data_dist['os'])

            if data_dist['status']=='Stopped':
                status = 0
            else:
                status = 1
            if not query.exists(): # 如果不存在
                detail_instance = HostDetail.objects.create(aliyun_id=data_dist['recognition_id'], info='', position=position,
                                                            systemtype=systype)
                host_instance = Host.objects.create(
                    detail=detail_instance,
                    connect_ip=data_dist['connect_ip'],
                    hostname=data_dist['instancename'],
                    status=status,
                    password='nopassword'
                )
            else:
                host_instance = query.get()
                host_instance.detail.save()
                host_instance.status = status
                host_instance.save()


# @periodic_task(run_every=crontab(minute=0,hour=[0,3,6,9,12,15,18,21]))
@periodic_task(run_every=crontab(minute=55,hour=0))
def vmwareInfoCatch():
    from deveops.utils import vmware
    children = vmware.fetch_AllInstance()
    position = None
    systype = None
    if Position.objects.filter(name__contains='集团内').exists():
        position = Position.objects.filter(name__contains='集团内').get()
    else:
        position = Position.objects.create(name='集团内')

    for child in children:
        '''
        {'privateMemory': 8500,
        'powerState': 'poweredOn', 'name': 'DWETL02', 'uptimeSeconds': 12389645, 'numCpu': 8, 'overallCpuUsage': 0,
        'memoryMB': 16384, 'memorySizeMB': 16384, 'guestMemoryUsage': 0, 'committed': 24335576477L, 'hostMemoryUsage': 9265,
         'ipAddress': '10.100.63.69', 'sharedMemory': 1662, 'unshared': 24212668416L}
        '''
        list = vmware.FetchInfo(child)
        status = 1
        if not list['powerState'] == 'poweredOn':
            status = 0
            continue

        if System_Type.objects.filter(name=list['guestFullName']).count() ==0:
            systype = System_Type.objects.create(name=list['guestFullName'])
        else:
            systype = System_Type.objects.filter(name=list['guestFullName']).get()

        if not list.__contains__('ipAddress'):
            continue
        if list['ipAddress'] is None:
            continue

        query = Host.objects.filter(detail__vmware_id=list['uuid'] ,connect_ip=list['ipAddress'])
        if not query.exists():
            detail_instance = HostDetail.objects.create(vmware_id=list['uuid'], info='', position=position, systemtype=systype)
            host_instance = Host.objects.create(
                detail=detail_instance,
                connect_ip=list['ipAddress'],
                hostname=list['name'],
                status=status,
                password='nopassword'
            )
        else:
            host_instance = query.get()
            host_instance.detail.save()
            host_instance.status = status
            host_instance.save()