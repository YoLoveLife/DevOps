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

def host_maker(dict_models):
    systype_query = System_Type.objects.filter(name=dict_models['detail']['systemtype'])
    if not systype_query.exists():
        systype = System_Type.objects.create(name=dict_models['detail']['systemtype'])
        dict_models['detail']['systemtype'] = systype
    else:
        dict_models['detail']['systemtype'] = systype_query.get()

    position_query = Position.objects.filter(name=dict_models['detail']['position'])
    if not position_query.exists():
        posistion = Position.objects.create(name=dict_models['detail']['position'])
        dict_models['detail']['position'] = posistion
    else:
        dict_models['detail']['position'] = position_query.get()

    detail_dict = dict_models.pop('detail')
    detail = HostDetail.objects.create(**detail_dict)
    dict_models['detail'] = detail

    host = Host.objects.create(**dict_models)


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
        results = API.get_instances(page)
        for result in results.get('Instances').get('Instance'):
            dict_models = API.get_aliyun_models(result)
            host_query = Host.objects.filter(detail__aliyun_id=dict_models['detail']['aliyun_id'], connect_ip=dict_models['connect_ip'])
            if not host_query.exists():
                host_maker(dict_models)


connect = redis.StrictRedis(host=settings.REDIS_HOST,port=settings.REDIS_PORT,db=settings.REDIS_SPACE,password=settings.REDIS_PASSWD)


@periodic_task(run_every=crontab(minute='*'))
def statistics():
    connect.delete('MANAGER_STATUS')

    status = {}
    # 資產計數
    status['host_count'] = Host.objects.count()
    status['group_count'] = Group.objects.count()

    # 類型統計
    systypes = System_Type.objects.all()
    sys_list = []
    for sys in systypes:
        sys_list.append({'name': sys.name,'value': sys.hosts_detail.count()})
    status['systemtype'] = sys_list
    # 不同系统类型所涉及的主机个数

    positions = Position.objects.all()
    pos_list = []
    for pos in positions:
        pos_list.append({'name': pos.name,'value': pos.hosts_detail.count()})
    status['position'] = pos_list
    # 不同位置所涉及的主机个数

    groups = Group.objects.all()
    group_list = []
    for group in groups:
        group_list.append({'name': group.name,'value': group.hosts.count()})
    status['groups'] = group_list

    status_json = json.dumps(status)
    connect.set('MANAGER_STATUS',status_json)
    print('get',connect.get('MANAGER_STATUS'))