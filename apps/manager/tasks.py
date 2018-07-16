# -*- coding:utf-8 -*-
# !/usr/bin/env python
# Time 17-10-25
# Author Yo
# Email YoLoveLife@outlook.com

from celery.task import periodic_task
from celery.schedules import crontab
from manager.models import Host,HostDetail,Position,System_Type,Group
from django.conf import settings
import redis, json
from timeline.decorator import decorator_task

def host_maker(dict_models):
    systype_query = System_Type.objects.filter(name=dict_models['detail']['systemtype'])
    if not systype_query.exists():
        systype = System_Type.objects.create(name=dict_models['detail']['systemtype'])
        dict_models['detail']['systemtype'] = systype
    else:
        dict_models['detail']['systemtype'] = systype_query[0]

    position_query = Position.objects.filter(name=dict_models['detail']['position'])
    if not position_query.exists():
        posistion = Position.objects.create(name=dict_models['detail']['position'])
        dict_models['detail']['position'] = posistion
    else:
        dict_models['detail']['position'] = position_query[0]

    detail_dict = dict_models.pop('detail')
    detail = HostDetail.objects.create(**detail_dict)
    dict_models['detail'] = detail

    host = Host.objects.create(**dict_models)


def host_updater(obj, dict_models):
    dict_models.pop('detail')
    dict_models['_status'] = dict_models.pop('status')
    obj.update(**dict_models)


@periodic_task(run_every=settings.MANAGER_TIME)
def vmware2cmdb():
    from deveops.tools import vmware
    API = vmware.VmwareTool()
    childrens = API.get_all_vms()
    for child in childrens:
        dict_models = API.get_vm_models(child)
        host_query = Host.objects.filter(detail__vmware_id=dict_models['detail']['vmware_id'], connect_ip=dict_models['connect_ip'])
        if not host_query.exists():
            host_maker(dict_models)


@periodic_task(run_every=settings.MANAGER_TIME)
def aliyun2cmdb():
    from deveops.tools.aliyun import ecs
    API = ecs.AliyunECSTool()
    for page in range(1,API.pagecount+1):
        results = API.request_get_instances(page)
        for result in results:
            dict_models = API.get_aliyun_models(result)
            host_query = Host.objects.filter(detail__aliyun_id=dict_models['detail']['aliyun_id'], connect_ip=dict_models['connect_ip'])
            if not host_query.exists():
                host_maker(dict_models)
            else:
                host_updater(host_query,dict_models)


@periodic_task(run_every=settings.MANAGER_TIME)
def cmdb2aliyun():
    from deveops.tools.aliyun import ecs
    from django.db.models import Q
    API = ecs.AliyunECSTool()
    queryset = Host.objects.filter(~Q(detail__aliyun_id=''))
    for host in queryset:
        status_results = API.request_get_instance_status(host.detail.aliyun_id)
        status = API.get_aliyun_instance_status(status_results)
        if status == 'delete':
            host.delete()
        else:
            expired_results = API.request_get_instance(host.detail.aliyun_id)
            expired = API.get_aliyun_expired_models(expired_results)
            if expired.get('expired') < settings.ALIYUN_OVERDUETIME:
                host.delete()
            else:
                host.status = status


connect = redis.StrictRedis(host=settings.REDIS_HOST,port=settings.REDIS_PORT,db=settings.REDIS_SPACE,password=settings.REDIS_PASSWD)


@periodic_task(run_every=crontab(minute='*/5'))
def statistics_systemtype():
    connect.delete('SYSTEMTYPE_STATUS')
    systypes = System_Type.objects.all()
    sys_name = []
    sys_value = []
    for sys in systypes:
        sys_name.append(sys.name)
        sys_value.append(sys.hosts_detail.count())

    connect.set('SYSTEMTYPE_STATUS', {"name":sys_name,"value":sys_value})

@periodic_task(run_every=crontab(minute='*/5'))
def statistics_group():
    connect.delete('GROUP_STATUS')

    groups = Group.objects.all()
    group_name = []
    group_value = []
    for group in groups:
        group_name.append(group.name)
        group_value.append(group.hosts.count())
    connect.set('GROUP_STATUS', {'name':group_name,'value':group_value})

@periodic_task(run_every=crontab(minute='*/5'))
def statistics_position():
    connect.delete('POSITION_STATUS')

    positions = Position.objects.all()
    position_name = []
    position_value = []
    for pos in positions:
        position_name.append(pos.name)
        position_value.append(pos.hosts_detail.count())
    connect.set('POSITION_STATUS', {'name':position_name,'value':position_value})


@periodic_task(run_every=crontab(minute='*/5'))
def statistics_manager():
    host_count = Host.objects.count()
    group_count = Group.objects.count()

    connect.set('HOST_COUNT', host_count)
    connect.set('GROUP_COUNT', group_count)
