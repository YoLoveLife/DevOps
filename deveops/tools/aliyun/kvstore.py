# -*- coding:utf-8 -*-
# !/usr/bin/env python
# Time 18-7-2
# Author WZZ
# import os
# import django
# os.environ.setdefault("DJANGO_SETTINGS_MODULE", "deveops.settings")
# django.setup()

import json
from aliyunsdkcore import client
from aliyunsdkr_kvstore.request.v20150101 import DescribeInstancesRequest
from django.conf import settings
import datetime


class AliyunKVStoreTool(object):
    def __init__(self):
        self.clt = client.AcsClient(settings.ALIYUN_ACCESSKEY, settings.ALIYUN_ACCESSSECRET, 'cn-hangzhou')
        self.pagecount = self.request_get_page_number()

    @staticmethod
    def get_json_results(results):
        return json.loads(results.decode('utf-8'))

    @staticmethod
    def request_to_json(request):
        return request.set_accept_format('json')

    def request_get_page_number(self):
        request = DescribeInstancesRequest.DescribeInstancesRequest()
        request.add_query_param('PageNumber', 1)
        request.add_query_param('PageSize', 1)
        try:
            response = self.clt.do_action_with_exception(request)
        except:
            return {}
        result = self.get_json_results(response)
        return int(result.get('TotalCount')/settings.ALIYUN_PAGESIZE)+1

    def request_get_instance(self, instance_id):
        request = DescribeInstancesRequest.DescribeInstancesRequest()
        self.request_to_json(request)
        request.add_query_param('RegionId', 'cn-hangzhou')
        request.add_query_param('InstanceIds', instance_id)
        try:
            response = self.clt.do_action_with_exception(request)
        except:
            return {}
        return self.get_json_results(response).get('Instances').get('KVStoreInstance')[0]

    def request_get_instances(self, page):
        request = DescribeInstancesRequest.DescribeInstancesRequest()
        self.request_to_json(request)
        request.add_query_param('RegionId', 'cn-hangzhou')
        request.add_query_param('PageNumber', page)
        request.add_query_param('PageSize', settings.ALIYUN_PAGESIZE)
        try:
            response = self.clt.do_action_with_exception(request)
        except:
            return {}
        return self.get_json_results(response).get('Instances').get('KVStoreInstance')

    @staticmethod
    def get_expired_day(time):
        expired = datetime.datetime.strptime(time, '%Y-%m-%dT%H:%M:%SZ')
        return (expired-datetime.datetime.now()).days

    @staticmethod
    def get_aliyun_expired_models(json_results):
        return {
            'expired': AliyunKVStoreTool.get_expired_day(json_results.get('EndTime')),
            'recognition_id': json_results.get('InstanceId'),
            'instancename': json_results.get('InstanceName'),
            'version': json_results.get('EngineVersion'),
            'connect_domain': json_results.get('ConnectionDomain'),
            'type': json_results.get('InstanceType'),
            'status': 'Running'
        }

    # @staticmethod
    # def get_aliyun_models(json_results):
    #     return {
    #         'aliyun_id': json_results.get('DBInstanceId'),
    #         'name': json_results.get('DBInstanceDescription')
    #     }