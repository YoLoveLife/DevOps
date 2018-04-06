# -*- coding:utf-8 -*-
# !/usr/bin/env python
# Time 17-10-25
# Author Yo
# Email YoLoveLife@outlook.com

from __future__ import absolute_import, unicode_literals
from celery.task import periodic_task
from celery.schedules import crontab
from manager.models import Host,HostDetail,Position,System_Type

# @periodic_task(run_every=crontab(minute=0,hour=[0,3,6,9,12,15,18,21]))
@periodic_task(run_every=crontab(minute='*'))
def vmwareInfoCatch():
    print('ZZCDDR-PPQ')
    from deveops.utils import vmware
    children = vmware.fetch_AllInstance()
    position = None
    win_systype = None
    centos_systype = None
    if Position.objects.filter(name__contains='集团').exists():
        position = Position.objects.filter(name__contains='集团').get()
    else:
        position = Position.objects.create(name='集团内')

    if System_Type.objects.filter(name__contains='Windows').exists():
        win_systype = System_Type.objects.filter(name__contains='Windows').get()
    else:
        win_systype = System_Type.objects.create(name='Windows')

    if System_Type.objects.filter(name__contains='Linux').exists():
        centos_systype = System_Type.objects.filter(name__contains='Linux').get()
    else:
        centos_systype = System_Type.objects.create(name='Linux')

    for child in children:
        '''
        {'privateMemory': 8500, 
        'powerState': 'poweredOn', 'name': 'DWETL02', 'uptimeSeconds': 12389645, 'numCpu': 8, 'overallCpuUsage': 0, 
        'memoryMB': 16384, 'memorySizeMB': 16384, 'guestMemoryUsage': 0, 'committed': 24335576477L, 'hostMemoryUsage': 9265,
         'ipAddress': '10.100.63.69', 'sharedMemory': 1662, 'unshared': 24212668416L}
        '''
        list = vmware.FetchInfo(child)
        status = 1
        os = None
        if not list['powerState'] == 'poweredOn':
            status = 0
        if list['guestFullName'].lower().find('windows') != -1:
            os = win_systype
        else:
            os = centos_systype
        if list['ipAddress'] is None:
            continue
        query = Host.objects.filter(detail__vmware_id=list['uuid'] ,connect_ip=list['ipAddress'])
        if not query.exists():
            detail_instance = HostDetail.objects.create(vmware_id=list['uuid'], info='', position=position, systemtype=os)
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