# -*- coding:utf-8 -*-
# !/usr/bin/env python
# Time 18-7-2
# Author Yo
import datetime
from deveops.tools.aliyun_v2.analyze.base import AnalyzeTool
from django.conf import settings


class AnalyzeECSTool(AnalyzeTool):

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
    def get_models(json_results):
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
            'status': AnalyzeECSTool.get_ecs_status(json_results.get('Status')),
            'systemtype': json_results.get('OSName'),
            'position': '阿里云',
            'aliyun_id': json_results.get('InstanceId'),
        }

    @staticmethod
    def get_expired_models(json_results):
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
            'expired': AnalyzeECSTool.get_expired_day(json_results.get('ExpiredTime')),
            'recognition_id': json_results.get('InstanceId'),
            'instancename': json_results.get('InstanceName'),
            'tags': ':'.join(tags_list),
            'status': json_results.get('Status')
        }

    @staticmethod
    def get_security_models(json_results):
        return {
            'security_id': json_results.get('SecurityGroupId'),
            'security_name': json_results.get('SecurityGroupName'),
            'vpc_id': json_results.get('VpcId')
        }