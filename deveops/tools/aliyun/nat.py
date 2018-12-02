# -*- coding:utf-8 -*-
# !/usr/bin/env python
# Time 18-7-3
# Author Yo
# Email YoLoveLife@outlook.com
import os
import django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "deveops.settings")
django.setup()

import json, datetime
from aliyunsdkcore import client
from aliyunsdkcore.request import CommonRequest
from django.conf import settings

class AliyunNATTool(object):
    def __init__(self):
        self.clt = client.AcsClient(settings.ALIYUN_ACCESSKEY, settings.ALIYUN_ACCESSSECRET, 'cn-hangzhou')

    @staticmethod
    def get_json_results(results):
        return json.loads(results.decode('utf-8'))

    @staticmethod
    def request_to_json(request):
        return request.set_accept_format('json')

    def request_get_gateway(self, gw_id):
        request = CommonRequest()
        self.request_to_json(request)
        request.set_domain('vpc.aliyuncs.com')
        request.set_version('2016-04-28')
        request.set_action_name('DescribeNatGateways')
        request.add_query_param('RegionId', 'cn-hangzhou')
        request.add_query_param('NatGatewayId', gw_id)
        try:
            response = self.clt.do_action_with_exception(request)
        except Exception as e:
            return []
        return self.get_json_results(response).get('NatGateways').get('NatGateway')

    def request_get_dnat(self, dnat_id):
        request = CommonRequest()
        self.request_to_json(request)
        request.set_domain('vpc.aliyuncs.com')
        request.set_version('2016-04-28')
        request.set_action_name('DescribeForwardTableEntries')
        request.add_query_param('RegionId', 'cn-hangzhou')
        request.add_query_param('ForwardTableId', dnat_id)
        try:
            response = self.clt.do_action_with_exception(request)

        except Exception as e:
            return []
        return self.get_json_results(response).get('ForwardTableEntries').get('ForwardTableEntry')

    def get_ipool_snat_models(self, result, info):
        address_list = result['SnatIp'].split('.')

        return {
            'A_address': address_list[0],
            'B_address': address_list[1],
            'C_address': address_list[2],
            'D_address': address_list[3],
            'type': settings.TYPE_IP_POOL_SNAT,
            'info': info
        }

    def get_ipool_dnat_models(self, result, info):
        inter_address_list = result['InternalIp'].split('.')
        exter_address_list = result['ExternalIp'].split('.')
        return [{
            'A_address': inter_address_list[0],
            'B_address': inter_address_list[1],
            'C_address': inter_address_list[2],
            'D_address': inter_address_list[3],
            'type': settings.TYPE_IP_POOL_DNAT,
            'info': info+' 端口{inter_port} 外部映射IP{exter_ip} 外部映射端口{exter_port}'.format(
                inter_port = result['InternalPort'],
                exter_ip = result['ExternalIp'],
                exter_port =result['ExternalPort']
            ),
        },{
            'A_address': exter_address_list[0],
            'B_address': exter_address_list[1],
            'C_address': exter_address_list[2],
            'D_address': exter_address_list[3],
            'type': settings.TYPE_IP_POOL_DNAT,
            'info': info+ ' 端口{exter_port} 内部映射IP{inter_ip} 内部映射端口{inter_port}'.format(
                exter_port = result['ExternalPort'],
                inter_ip = result['InternalIp'],
                inter_port = result['InternalPort']
            )
        }]

    def request_get_snat(self, snat_id):
        request = CommonRequest()
        self.request_to_json(request)
        request.set_domain('vpc.aliyuncs.com')
        request.set_version('2016-04-28')
        request.set_action_name('DescribeSnatTableEntries')
        request.add_query_param('RegionId', 'cn-hangzhou')
        request.add_query_param('SnatTableId', snat_id)

        try:
            response = self.clt.do_action_with_exception(request)
        except Exception as e:
            print(e)
            return {}
        return self.get_json_results(response).get('SnatTableEntries').get('SnatTableEntry')




API = AliyunNATTool()
print(API.request_get_gateway('vpc-bp1hqvm6iacurg4sjn5ki'))
