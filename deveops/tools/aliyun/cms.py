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
    def request_to_day(obj):
        now = datetime.datetime.now().strftime('%Y-%m-%d 00:00:00')
        seven = (datetime.datetime.now() - datetime.timedelta(days=2)).strftime('%Y-%m-%d 00:00:00')
        obj.request.add_query_param('StartTime', seven)
        obj.request.add_query_param('EndTime', now)

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

    def get_cpu_results(self):
        pass

    def get_mem_results(self):
        pass

    def get_load_results(self):
        pass

    @staticmethod
    def get_line_opts(results, title):
        import datetime
        time = []
        minimum = []
        maximum = []
        for result in json.loads(results):
            d = datetime.datetime.fromtimestamp(result['timestamp']/1000)
            str1 = d.strftime("%Y-%m-%d %H:%M")
            time.append(str1)
            minimum.append(result['Minimum'])
            maximum.append(result['Maximum'])
            # average.append(result['Average'])
        from pyecharts import Line
        from pyecharts.base import TRANSLATOR
        line = Line(title)
        line.add("最小值", time, minimum, mark_point=['max'], mark_line=["average",], )
        # line.add("平均值", time, average, mark_point=["average", "min"])
        line.add("最大值", time, maximum, mark_point=['max'], mark_line=["average",], )
        snippet = TRANSLATOR.translate(line.options)
        return json.loads(snippet.as_snippet())


class AliyunECSCMSTool(AliyunCMSTool):
    def __init__(self):
        super(AliyunECSCMSTool, self).__init__()
        AliyunECSCMSTool.request_to_ecs_dashboard(self)

    def get_cpu_results(self):
        AliyunCMSTool.request_to_metric(self, 'CPUUtilization')

    def get_mem_results(self):
        AliyunCMSTool.request_to_metric(self, 'memory_usedutilization')


class AliyunRDSCMSTool(AliyunCMSTool):
    def __init__(self):
        super(AliyunRDSCMSTool, self).__init__()
        AliyunRDSCMSTool.request_to_rds_dashboard(self)

    def get_cpu_results(self):
        AliyunCMSTool.request_to_metric(self, 'CpuUsage')

    def get_mem_results(self):
        AliyunCMSTool.request_to_metric(self, 'MemoryUsage')

