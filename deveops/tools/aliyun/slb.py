# -*- coding:utf-8 -*-
# !/usr/bin/env python
# Time 18-7-2
# Author WZZ
import os
import django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "deveops.settings")
django.setup()

import json
import datetime
from aliyunsdkcore import client
from aliyunsdkcore.request import CommonRequest
from django.conf import settings


class AliyunSLBTool(object):
    def __init__(self):
        self.clt = client.AcsClient(settings.ALIYUN_ACCESSKEY, settings.ALIYUN_ACCESSSECRET, 'cn-hangzhou')
        self.pagecount = self.request_get_page_number()

    @staticmethod
    def request_to_json(request):
        return request.set_accept_format('json')

    @staticmethod
    def get_json_results(results):
        return json.loads(results.decode('utf-8'))


    @staticmethod
    def get_ipool_models(json_results):
        try:
            if '.' in json_results.get('Address'):
                ip_address = json_results.get('Address')
                address_list = ip_address.split('.')
                return {
                    'A_address':address_list[0],
                    'B_address':address_list[1],
                    'C_address':address_list[2],
                    'D_address':address_list[3],
                    'type': settings.TYPE_IP_POOL_SLB,
                    'info': 'SLB实例:{LoadBalancerName} 实例ID:{LoadBalancerId}'.format(
                        LoadBalancerName=json_results.get('LoadBalancerName'),
                        LoadBalancerId = json_results.get('LoadBalancerId'),
                    )
                }
            else:
                return {}
        except Exception as e:
            return {}


    def request_get_slbs(self, page):
        request = CommonRequest()
        self.request_to_json(request)
        request.set_domain('slb.aliyuncs.com')
        request.set_method('POST')
        request.set_version('2014-05-15')
        request.set_action_name('DescribeLoadBalancers')
        request.add_query_param('RegionId', 'cn-hangzhou')
        request.add_query_param('PageNumber', page)
        request.add_query_param('PageSize', settings.ALIYUN_PAGESIZE)
        try:
            response = self.clt.do_action_with_exception(request)
        except:
            return []
        return self.get_json_results(response).get('LoadBalancers').get('LoadBalancer')


    def request_get_page_number(self):
        request = CommonRequest()
        self.request_to_json(request)
        request.set_domain('slb.aliyuncs.com')
        request.set_method('POST')
        request.set_version('2014-05-15')
        request.set_action_name('DescribeLoadBalancers')
        request.add_query_param('RegionId', 'cn-hangzhou')
        request.add_query_param('PageNumber', 1)
        request.add_query_param('PageSize', 1)
        try:
            response = self.clt.do_action_with_exception(request)
        except:
            return 1
        result = self.get_json_results(response)
        return int(result['TotalCount']/settings.ALIYUN_PAGESIZE)+1



