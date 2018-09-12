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
        self.request = CommonRequest()
        AliyunNATTool.request_to_json(self)

    @staticmethod
    def get_json_results(results):
        return json.loads(results.decode('utf-8'))

    @staticmethod
    def request_to_json(obj):
        return obj.request.set_accept_format('json')

    def request_to_gateway(self):
        self.request.set_domain('vpc.aliyuncs.com')
        self.request.set_version('2016-04-28')
        self.request.set_action_name('DescribeNatGateways')
        self.request.add_query_param('RegionId', 'cn-hangzhou')

        try:
            response = self.clt.do_action_with_exception(self.request)
        except Exception as e:
            print(e)
            return {}
        return self.get_json_results(response)

    def request_to_dnat(self, dnat_id):
        self.request.set_domain('vpc.aliyuncs.com')
        self.request.set_version('2016-04-28')
        self.request.set_action_name('DescribeForwardTableEntries')
        self.request.add_query_param('RegionId', 'cn-hangzhou')
        self.request.add_query_param('ForwardTableId', dnat_id)

        try:
            response = self.clt.do_action_with_exception(self.request)
        except Exception as e:
            print(e)
            return {}
        return self.get_json_results(response)