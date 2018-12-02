# -*- coding:utf-8 -*-
# !/usr/bin/env python
# Time 18-9-14
# Author Yo
import datetime
from deveops.tools.aliyun_v2.request.base import AliyunTool
from django.conf import settings


class AliyunCMSTool(AliyunTool):
    def init_action(self):
        self.request.set_domain('metrics.cn-hangzhou.aliyuncs.com')
        self.request.set_method('POST')
        self.request.set_version('2018-03-08')

    def action_get_metric(self):
        self.init()
        self.request.set_action_name('QueryMetricData')

    def tool_get_metric_hour(self, hours):
        now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        seven = (datetime.datetime.now() - datetime.timedelta(hours=hours)).strftime('%Y-%m-%d %H:%M:%S')
        self.request.add_query_param('StartTime', seven)
        self.request.add_query_param('EndTime', now)
        self.request.add_query_param('Period', '60')

    def tool_get_metric_day(self, days):
        now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        seven = (datetime.datetime.now() - datetime.timedelta(days=days)).strftime('%Y-%m-%d %H:%M:%S')
        self.request.add_query_param('StartTime', seven)
        self.request.add_query_param('EndTime', now)
        self.request.add_query_param('Period', '900')

    def tool_get_metric_1hour(self):
        self.tool_get_metric_hour(1)

    def tool_get_metric_6hour(self):
        self.tool_get_metric_hour(6)

    def tool_get_metric_12hour(self):
        self.tool_get_metric_hour(12)

    def tool_get_metric_1day(self):
        self.tool_get_metric_day(1)

    def tool_get_metric_3day(self):
        self.tool_get_metric_day(3)

    def tool_get_metric_7day(self):
        self.tool_get_metric_day(7)

    def time_select(self, time):
        if time == settings.TYPE_MONITOR_ONE_HOUR:
            self.tool_get_metric_1hour()
        elif time == settings.TYPE_MONITOR_SIX_HOUR:
            self.tool_get_metric_6hour()
        elif time == settings.TYPE_MONITOR_HALF_DAY:
            self.tool_get_metric_12hour()
        elif time == settings.TYPE_MONITOR_DAY:
            self.tool_get_metric_1day()
        elif time == settings.TYPE_MONITOR_3_DAY:
            self.tool_get_metric_3day()
        elif time == settings.TYPE_MONITOR_7_DAY:
            self.tool_get_metric_7day()
        else:
            pass

