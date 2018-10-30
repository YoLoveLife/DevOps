# -*- coding:utf-8 -*-
# !/usr/bin/env python
# Time 18-7-2
# Author WZZ
import os
import django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "deveops.settings")
django.setup()

import json
from aliyunsdkcore import client
from aliyunsdkcore.request import CommonRequest
from django.conf import settings


class AliyunSecurityGroupTool(object):
    def __init__(self, vpc_id):
        self.clt = client.AcsClient(settings.ALIYUN_ACCESSKEY, settings.ALIYUN_ACCESSSECRET, 'cn-hangzhou')
        self.pagecount = self.request_get_page_number(vpc_id)

    @staticmethod
    def request_to_json(request):
        return request.set_accept_format('json')

    @staticmethod
    def get_json_results(results):
        return json.loads(results.decode('utf-8'))


    def request_get_securitygroups(self, vpc_id, page):
        request = CommonRequest()
        self.request_to_json(request)
        request.set_domain('ecs.aliyuncs.com')
        request.set_method('POST')
        request.set_version('2014-05-26')
        request.set_action_name('DescribeSecurityGroups')

        request.add_query_param('RegionId', 'cn-hangzhou')
        request.add_query_param('VpcId', vpc_id)
        request.add_query_param('PageNumber', page)
        request.add_query_param('PageSize', settings.ALIYUN_PAGESIZE)
        try:
            response = self.clt.do_action_with_exception(request)
        except:
            return []
        return self.get_json_results(response).get('SecurityGroups').get('SecurityGroup')

    def request_get_securitygroup_rules(self):
        request = CommonRequest()
        self.request_to_json(request)

    def request_get_page_number(self, vpc_id):
        request = CommonRequest()
        self.request_to_json(request)
        request.set_domain('ecs.aliyuncs.com')
        request.set_method('POST')
        request.set_version('2014-05-26')
        request.set_action_name('DescribeSecurityGroups')

        request.add_query_param('RegionId', 'cn-hangzhou')
        request.add_query_param('VpcId', vpc_id)
        request.add_query_param('PageNumber', 1)
        request.add_query_param('PageSize', 1)
        try:
            response = self.clt.do_action_with_exception(request)
        except:
            return 1
        result = self.get_json_results(response)
        return int(result['TotalCount']/settings.ALIYUN_PAGESIZE)+1



