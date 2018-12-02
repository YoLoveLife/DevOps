# -*- coding:utf-8 -*-
# !/usr/bin/env python
# Time 18-11-08
# Author Yo
from deveops.tools.aliyun_v2.request.base import AliyunTool
from django.conf import settings


class AliyunDNSTool(AliyunTool):
    def init_action(self):
        self.request.set_domain('pvtz.aliyuncs.com')
        self.request.set_method('GET')
        self.request.set_version('2018-01-01')

    def action_get_zone(self):
        self.init()
        self.request.set_action_name('DescribeZones')

    def action_check_zone(self):
        self.init()
        self.request.set_action_name('CheckZoneName')

    def action_add_zone(self):
        self.init()
        self.request.set_action_name('AddZone')

    def action_add_record(self):
        self.init()
        self.request.set_action_name('AddZoneRecord')

    def action_update_record(self):
        self.init()
        self.request.set_action_name('UpdateZoneRecord')

    def tool_get_zones(self):
        self.action_get_zone()
        print(self.post())

    def tool_check_zone(self, zonename):
        self.action_check_zone()
        self.request.add_query_param(
            'ZoneName', zonename
        )
        print(self.post())

    def tool_add_zone(self, zonename):
        self.action_add_zone()
        self.request.add_query_param(
            'ZoneName', zonename
        )
        print(self.post())

    def tool_add_record(self, *args, **kwargs):
        self.action_add_record()
        for arg in kwargs:
            self.request.add_query_param(
                arg, kwargs[arg]
            )
        print(self.post())

    def tool_update_record(self, *args, **kwargs):
        self.action_update_record()
        for arg in kwargs:
            self.request.add_query_param(
                arg, kwargs[arg]
            )
        print(self.post())