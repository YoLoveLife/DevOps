# -*- coding:utf-8 -*-
# !/usr/bin/env python
# Time 17-10-25
# Author Yo
# Email YoLoveLife@outlook.com
import redis
from celery.task import periodic_task
from celery.schedules import crontab
from django.conf import settings
from manager.models import Host,Group

def host_maker(dict_models):
    Host.objects.create(**dict_models)


def host_updater(obj, dict_models):
    status = dict_models.pop('status')
    if obj.get().status == settings.STATUS_HOST_PAUSE:
        if status == settings.STATUS_HOST_CAN_BE_USE:
            pass
        else:
            dict_models['_status'] = settings.STATUS_HOST_CLOSE
    else:
        dict_models['_status'] = status

    obj.update(**dict_models)


@periodic_task(run_every=settings.MANAGER_TIME)
def vmware2cmdb():
    from deveops.tools import vmware
    API = vmware.VmwareTool()
    childrens = API.get_all_vms()
    for child in childrens:
        dict_models = API.get_vm_models(child)
        host_query = Host.objects.filter(vmware_id=dict_models['vmware_id'], connect_ip=dict_models['connect_ip'])
        if not host_query.exists():
            host_maker(dict_models)


@periodic_task(run_every=settings.MANAGER_TIME)
def aliyun2cmdb():
    from deveops.tools.aliyun import ecs
    API = ecs.AliyunECSTool()
    for page in range(1, API.pagecount+1):
        results = API.request_get_instances(page)
        for result in results:
            dict_models = API.get_aliyun_models(result)
            host_query = Host.objects.filter(aliyun_id=dict_models['aliyun_id'], connect_ip=dict_models['connect_ip'])
            if not host_query.exists():
                host_maker(dict_models)
            else:
                host_updater(host_query, dict_models)


@periodic_task(run_every=settings.MANAGER_TIME)
def cmdb2aliyun():
    from deveops.tools.aliyun import ecs
    from django.db.models import Q
    API = ecs.AliyunECSTool()
    queryset = Host.objects.filter(~Q(detail__aliyun_id=''))
    for host in queryset:
        status_results = API.request_get_instance_status(host.aliyun_id)
        status = API.get_aliyun_instance_status(status_results)
        if status == 'delete':
            host.delete()
        else:
            expired_results = API.request_get_instance(host.aliyun_id)
            expired = API.get_aliyun_expired_models(expired_results)
            if expired.get('expired') < settings.ALIYUN_OVERDUETIME:
                host.delete()
            else:
                if host.status == settings.STATUS_HOST_PAUSE:
                    if status == settings.STATUS_HOST_CAN_BE_USE:
                        pass
                    else:
                        host.status = settings.STATUS_HOST_CLOSE
                else:
                    host.status = status



connect = redis.StrictRedis(host=settings.REDIS_HOST,port=settings.REDIS_PORT,db=settings.REDIS_SPACE,password=settings.REDIS_PASSWD)


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
def statistics_manager():
    host_count = Host.objects.count()
    group_count = Group.objects.count()

    connect.set('HOST_COUNT', host_count)
    connect.set('GROUP_COUNT', group_count)
