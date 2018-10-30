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
from aliyunsdkecs.request.v20140526 import DescribeInstancesFullStatusRequest,DescribeInstanceStatusRequest,DescribeInstancesRequest,DescribeInstanceAttributeRequest,DescribePriceRequest
from django.conf import settings


class AliyunECSTool(object):
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
    def get_ecs_status(status):
        if status == 'Running':
            return settings.STATUS_HOST_CAN_BE_USE
        else:
            return settings.STATUS_HOST_CLOSE

    @staticmethod
    def get_expired_day(time):
        expired = datetime.datetime.strptime(time, '%Y-%m-%dT%H:%MZ')
        return (expired-datetime.datetime.now()).days

    @staticmethod
    def get_aliyun_models(json_results):
        try:
            ipaddr = json_results.get('NetworkInterfaces').get('NetworkInterface')[0].get('PrimaryIpAddress')
        except AttributeError as e:
            ipaddr = json_results.get('PublicIpAddress').get('IpAddress')[0]
        if not ipaddr:
            ipaddr = json_results.get('VpcAttributes').get('PrivateIpAddress').get('IpAddress')[0]

        return {
            'hostname': json_results.get('InstanceName'),
            'connect_ip': ipaddr,
            'sshport': 22,
            'status': AliyunECSTool.get_ecs_status(json_results.get('Status')),
            'systemtype': json_results.get('OSName'),
            'position': '阿里云',
            'aliyun_id': json_results.get('InstanceId'),
        }

    @staticmethod
    def get_aliyun_expired_models(json_results):
        try:
            ipaddr = json_results.get('NetworkInterfaces').get('NetworkInterface')[0].get('PrimaryIpAddress')
        except AttributeError as e:
            if len(json_results.get('PublicIpAddress').get('IpAddress')) != 0:
                ipaddr = json_results.get('PublicIpAddress').get('IpAddress')[0]
            else:
                ipaddr = json_results.get('VpcAttributes').get('PrivateIpAddress').get('IpAddress')[0]

        tags_list = []
        if json_results.__contains__('Tags'):
            for tag in json_results['Tags']['Tag']:
                tags_list.append(tag['TagKey'] + tag['TagValue'])
        return {
            'connect_ip': ipaddr,
            'expired': AliyunECSTool.get_expired_day(json_results.get('ExpiredTime')),
            'recognition_id': json_results.get('InstanceId'),
            'instancename': json_results.get('InstanceName'),
            'tags': ':'.join(tags_list),
            'status': json_results.get('Status')
        }

    @staticmethod
    def get_aliyun_instance_status(json_results):
        try:
            status = json_results.get('InstanceFullStatusSet').get('InstanceFullStatusType')[0]
        except IndexError as e:
            return 'delete'

        return AliyunECSTool.get_ecs_status(status.get('Status').get('Name'))


    def request_get_page_number(self):
        request = DescribeInstanceStatusRequest.DescribeInstanceStatusRequest()
        request.add_query_param('PageNumber', 1)
        request.add_query_param('PageSize', 1)
        try:
            response = self.clt.do_action_with_exception(request)
        except:
            return {}
        result = self.get_json_results(response)
        return int(result['TotalCount']/settings.ALIYUN_PAGESIZE)+1


    def request_get_instance_status(self, instance_id):
        request = DescribeInstancesFullStatusRequest.DescribeInstancesFullStatusRequest()
        self.request_to_json(request)
        request.add_query_param('RegionId', 'cn-hangzhou')
        request.add_query_param('PageNumber', 1)
        request.add_query_param('InstanceId.1', instance_id)
        try:
            response = self.clt.do_action_with_exception(request)
        except:
            return {}
        return self.get_json_results(response)


    def request_get_instance(self, instance_id):
        # request = DescribeInstancesRequest.DescribeInstancesRequest()
        request = DescribeInstanceAttributeRequest.DescribeInstanceAttributeRequest()
        self.request_to_json(request)
        request.add_query_param('InstanceId', instance_id)
        try:
            response = self.clt.do_action_with_exception(request)
        except:
            return {}
        return self.get_json_results(response)

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
        return self.get_json_results(response).get('Instances').get('Instance')
