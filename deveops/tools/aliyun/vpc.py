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


class AliyunVPCTool(object):
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
    def request_to_common():
        request = CommonRequest()
        request.set_domain('vpc.aliyuncs.com')
        request.set_method('POST')
        request.set_version('2016-04-28')
        request.set_action_name('DescribeVpcs')
        request.add_query_param('RegionId', 'cn-hangzhou')
        return request

    def request_get_vpcs(self, page):
        request = self.request_to_common()
        self.request_to_json(request)
        request.add_query_param('PageNumber', page)
        request.add_query_param('PageSize', settings.ALIYUN_PAGESIZE)
        try:
            response = self.clt.do_action_with_exception(request)
        except:
            return []
        return self.get_json_results(response).get('Vpcs').get('Vpc')


    def request_get_page_number(self):
        request = self.request_to_common()
        self.request_to_json(request)
        request.add_query_param('PageNumber', 1)
        request.add_query_param('PageSize', 1)
        try:
            response = self.clt.do_action_with_exception(request)
        except Exception as e:
            return 1
        result = self.get_json_results(response)
        return int(result['TotalCount']/settings.ALIYUN_PAGESIZE)+1