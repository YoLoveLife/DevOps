# -*- coding:utf-8 -*-
# !/usr/bin/env python
# Time 18-9-14
# Author Yo
import datetime
from deveops.tools.aliyun_v2.request.cms.base import AliyunCMSTool
from deveops.tools.aliyun_v2.analyze.cms import AnalyzeCMSTool
from django.conf import settings

class AliyunCMSECSTool(AliyunCMSTool):
    def action_get_metric(self):
        super(AliyunCMSECSTool, self).action_get_metric()
        self.request.add_query_param('Project', 'acs_ecs_dashboard')

    def tool_get_metric_cpu(self, instance_id, time):
        self.action_get_metric()
        self.time_select(time)
        self.request.add_query_param('Metric', 'cpu_total')#'CPUUtilization')
        self.request.add_query_param('Dimensions', str({'instanceId': instance_id}))
        results = self.post()
        yield AnalyzeCMSTool.change_timestamp(results.get('Datapoints'))

    def tool_get_metric_mem(self, instance_id, time):
        self.action_get_metric()
        self.time_select(time)
        self.request.add_query_param('Metric', 'memory_usedutilization')
        self.request.add_query_param('Dimensions', str({'instanceId': instance_id}))
        results = self.post()
        yield AnalyzeCMSTool.change_timestamp(results.get('Datapoints'))

    def tool_get_metric_read_iops(self, instance_id, time):
        self.action_get_metric()
        self.time_select(time)
        self.request.add_query_param('Metric', 'DiskReadIOPS')
        self.request.add_query_param('Dimensions', str({'instanceId': instance_id}))
        results = self.post()
        yield AnalyzeCMSTool.change_timestamp(results.get('Datapoints'))

    def tool_get_metric_write_iops(self, instance_id, time):
        self.action_get_metric()
        self.time_select(time)
        self.request.add_query_param('Metric', 'DiskWriteIOS')
        self.request.add_query_param('Dimensions', str({'instanceId': instance_id}))
        results = self.post()
        yield AnalyzeCMSTool.change_timestamp(results.get('Datapoints'))

    def tool_get_metric_net_in(self, instance_id, time):
        self.action_get_metric()
        self.time_select(time)
        self.request.add_query_param('Metric', 'IntranetInRate')
        self.request.add_query_param('Dimensions', str({'instanceId': instance_id}))
        results = self.post()
        yield AnalyzeCMSTool.change_timestamp(results.get('Datapoints'))

    def tool_get_metric_net_out(self, instance_id, time):
        self.action_get_metric()
        self.time_select(time)
        self.request.add_query_param('Metric', 'IntranetOutRate')
        self.request.add_query_param('Dimensions', str({'instanceId': instance_id}))
        results = self.post()
        yield AnalyzeCMSTool.change_timestamp(results.get('Datapoints'))


    def tool_get_metric_disk_use(self, instance_id, time):
        self.action_get_metric()
        self.time_select(time)
        self.request.add_query_param('Metric', 'diskusage_used')
        self.request.add_query_param('Dimensions', str({'instanceId': instance_id,'device':'/dev/vda1'}))