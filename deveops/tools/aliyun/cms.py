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
from aliyunsdkcms.request.v20180308 import QueryMetricDataRequest
from django.conf import settings

class AliyunCMSTool(object):
    def __init__(self):
        self.clt = client.AcsClient(settings.ALIYUN_ACCESSKEY, settings.ALIYUN_ACCESSSECRET, 'cn-hangzhou')
        self.request = QueryMetricDataRequest.QueryMetricDataRequest()
        AliyunCMSTool.request_to_json(self)

    @staticmethod
    def get_json_results(results):
        return json.loads(results.decode('utf-8'))

    @staticmethod
    def request_to_json(obj):
        return obj.request.set_accept_format('json')

    @staticmethod
    def request_to_ecs_dashboard(obj):
        return obj.request.add_query_param('Project', 'acs_ecs_dashboard')

    @staticmethod
    def request_to_rds_dashboard(obj):
        return obj.request.add_query_param('Project', 'acs_rds_dashboard')

    @staticmethod
    def request_to_instance(obj, instance):
        return obj.request.add_query_param('Dimensions', str({'instanceId':instance}))

    @staticmethod
    def request_to_time(obj, startTime2endTime):
        time = startTime2endTime.split('to')
        obj.request.add_query_param('StartTime', '{DATE} 00:00:00'.format(DATE=time[0]))
        obj.request.add_query_param('EndTime', '{DATE} 00:00:00'.format(DATE=time[1]))


    @staticmethod
    def request_to_hour(obj, hour):
        now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        seven = (datetime.datetime.now() - datetime.timedelta(hours=hour)).strftime('%Y-%m-%d %H:%M:%S')
        obj.request.add_query_param('StartTime', seven)
        obj.request.add_query_param('EndTime', now)
        obj.request_to_period(obj, '60')


    @staticmethod
    def request_to_day(obj, day):
        now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        seven = (datetime.datetime.now() - datetime.timedelta(days=day)).strftime('%Y-%m-%d %H:%M:%S')
        obj.request.add_query_param('StartTime', seven)
        obj.request.add_query_param('EndTime', now)
        obj.request_to_period(obj, '900')

    @staticmethod
    def request_to_period(obj, period):
        return obj.request.add_query_param('Period', period)

    @staticmethod
    def request_to_metric(obj, metric):
        return obj.request.add_query_param('Metric', metric)

    def get_results(self):
        try:
            response = self.clt.do_action_with_exception(self.request)
        except:
            return {}
        return self.get_json_results(response).get('Datapoints')

    def request_get_cpu_results(self):
        pass

    def request_get_mem_results(self):
        pass

    def request_get_load_results(self):
        pass

    @staticmethod
    def change_timestamp(dataset):
        json_dataset = []
        for data in json.loads(dataset):
            d = datetime.datetime.fromtimestamp(data['timestamp'] / 1000)
            str1 = d.strftime("%Y/%m/%d %H:%M:%S")  # "%Y/%m/%d %H:%M:%S"
            data['timestamp'] = str1
            json_dataset.append(data)
        return json_dataset


class AliyunECSCMSTool(AliyunCMSTool):
    def __init__(self):
        super(AliyunECSCMSTool, self).__init__()
        AliyunECSCMSTool.request_to_ecs_dashboard(self)

    def request_get_cpu_results(self):
        AliyunCMSTool.request_to_metric(self, 'CPUUtilization')

    def request_get_mem_results(self):
        AliyunCMSTool.request_to_metric(self, 'memory_usedutilization')

    def request_get_read_iops_results(self):
        AliyunCMSTool.request_to_metric(self, 'DiskReadIOPS')

    def request_get_write_iops_results(self):
        AliyunCMSTool.request_to_metric(self, 'DiskWriteIOS')

    def request_get_in_net_results(self):
        AliyunCMSTool.request_to_metric(self, 'IntranetInRate')

    def request_get_out_net_results(self):
        AliyunCMSTool.request_to_metric(self, 'IntranetOutRate')


class AliyunRDSCMSTool(AliyunCMSTool):
    def __init__(self):
        super(AliyunRDSCMSTool, self).__init__()
        AliyunRDSCMSTool.request_to_rds_dashboard(self)

    def request_get_cpu_results(self):
        AliyunCMSTool.request_to_metric(self, 'CpuUsage')

    def request_get_mem_results(self):
        AliyunCMSTool.request_to_metric(self, 'MemoryUsage')

    def request_get_iops_results(self):
        AliyunCMSTool.request_to_metric(self, 'IOPSUsage')

    def request_get_connect_results(self):
        AliyunCMSTool.request_to_metric(self, 'ConnectionUsage')

    def request_get_delay_results(self):
        AliyunCMSTool.request_to_metric(self, 'DataDelay')