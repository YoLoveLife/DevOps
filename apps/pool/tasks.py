# -*- coding:utf-8 -*-
# !/usr/bin/env python
# Time 18-7-2
# Author Yo
import os
import django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "deveops.settings")
django.setup()
from celery.task import periodic_task
from celery.schedules import crontab
from django.conf import settings
from pool.models import IP_Pool



def ipool_maker(dict_models):
    IP_Pool.objects.create(**dict_models)



def vpcs_list():
    from deveops.tools.aliyun import vpc
    VPCAPI = vpc.AliyunVPCTool()
    for page in range(1, VPCAPI.pagecount+1):
        vpc_results = VPCAPI.request_get_vpcs(page)
        for vpc_result in vpc_results:
            yield vpc_result


def gws_list(vpc):
    pass


@periodic_task(run_every=settings.POOL_SLB)
def aliyun_slb_ipoll():
    from deveops.tools.aliyun import slb
    API = slb.AliyunSLBTool()
    for page in range(1, API.pagecount+1):
        results = API.request_get_slbs(page)
        for result in results:
            dict_models = API.get_ipool_models(result)
            if dict_models: # 排除IPV6
                ipool_query = IP_Pool.objects.filter(
                    A_address = dict_models['A_address'],
                    B_address = dict_models['B_address'],
                    C_address = dict_models['C_address'],
                    D_address = dict_models['D_address'],
                    type = dict_models['type'],
                    info = dict_models['info']
                )
                if not ipool_query.exists():
                    ipool_maker(dict_models)


@periodic_task(run_every=settings.POOL_GATEWAY)
def aliyun_gw_ipoll():
    from deveops.tools.aliyun import vpc,nat
    VPCAPI = vpc.AliyunVPCTool()
    for page in range(1, VPCAPI.pagecount+1):
        vpc_results = VPCAPI.request_get_vpcs(page)
        for vpc_result in vpc_results:
            gw_id = vpc_result['NatGatewayIds']['NatGatewayIds'][0]
            NATAPI = nat.AliyunNATTool()
            gw_results = NATAPI.request_get_gateway(gw_id)
            for gw_result in gw_results:
                dnat_id = gw_result['ForwardTableIds']['ForwardTableId'][0]
                snat_id = gw_result['SnatTableIds']['SnatTableId'][0]

                snat_results = NATAPI.request_get_snat(snat_id)
                for snat_result in snat_results:
                    dict_models = NATAPI.get_ipool_snat_models(
                        snat_result,
                        'VPC{name} 出口IP'.format(name=vpc_result['Description'])
                    )
                    ipool_query = IP_Pool.objects.filter(
                        A_address=dict_models['A_address'],
                        B_address=dict_models['B_address'],
                        C_address=dict_models['C_address'],
                        D_address=dict_models['D_address'],
                        type = dict_models['type'],
                        info = dict_models['info']
                    )
                    if not ipool_query.exists():
                        ipool_maker(dict_models)

                dnat_results = NATAPI.request_get_dnat(dnat_id)
                for dnat_result in dnat_results:
                    dict_models_list = NATAPI.get_ipool_dnat_models(
                        dnat_result,
                        'VPC{name}'.format(name=vpc_result['Description'])
                    )
                    for dict_models in dict_models_list:
                        ipool_query = IP_Pool.objects.filter(
                            A_address=dict_models['A_address'],
                            B_address=dict_models['B_address'],
                            C_address=dict_models['C_address'],
                            D_address=dict_models['D_address'],
                            type=dict_models['type'],
                            info=dict_models['info']
                        )
                        if not ipool_query.exists():
                            ipool_maker(dict_models)


def aliyun_security_pool():
    from deveops.tools.aliyun import vpc,securitygroup
    VPCAPI = vpc.AliyunVPCTool()
    for vpc_page in range(1, VPCAPI.pagecount+1):
        vpc_results = VPCAPI.request_get_vpcs(vpc_page)
        for vpc_result in vpc_results:
            vpc_id = vpc_result['VpcId']
            SECURITYAPI = securitygroup.AliyunSecurityGroupTool(vpc_id)
            for sg_page in range(1, SECURITYAPI.pagecount+1):
                sg_results = SECURITYAPI.request_get_securitygroups(vpc_id, sg_page)
                for sg_result in sg_results:
                    pass


@periodic_task(run_every=settings.POOL_HOST)
def host_ipoll():
    from manager.models import Host
    for host in Host.objects.all():
        address_list = host.connect_ip.split('.')
        dict_models = {
                    'A_address':address_list[0],
                    'B_address':address_list[1],
                    'C_address':address_list[2],
                    'D_address':address_list[3],
                    'type': settings.TYPE_IP_POOL_ECS,
                    'info': '资产主机实例:{hostname} 资产位置:{position} 资产所属:{group}'.format(
                        hostname = host.hostname,
                        position = host.position,
                        status = host.status,
                        group = host.group,
                    )
                }
        ipool_query = IP_Pool.objects.filter(
            A_address=dict_models['A_address'],
            B_address=dict_models['B_address'],
            C_address=dict_models['C_address'],
            D_address=dict_models['D_address'],
            type=dict_models['type'],
            info=dict_models['info']
        )
        if not ipool_query.exists():
            ipool_maker(dict_models)

