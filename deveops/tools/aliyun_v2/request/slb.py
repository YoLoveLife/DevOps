# -*- coding:utf-8 -*-
# !/usr/bin/env python
# Time 18-9-14
# Author Yo
from deveops.tools.aliyun_v2.request.base import AliyunTool
from deveops.tools.aliyun_v2.analyze.slb import AnalyzeSLBTool
from django.conf import settings


class AliyunSLBTool(AliyunTool):
    def init_action(self):
        self.request.set_domain('slb.aliyuncs.com')
        self.request.set_method('POST')
        self.request.set_version('2014-05-15')


    def action_get_slb(self):
        self.init()
        self.request.set_action_name('DescribeLoadBalancers')


    def tool_get_slbs(self):
        self.action_get_slb()
        for page in range(1, 9999):
            self.request.add_query_param('PageNumber', page)
            self.request.add_query_param('PageSize', settings.ALIYUN_PAGESIZE)
            results = self.post()

            for result in results.get('LoadBalancers').get('LoadBalancer'):
                yield AnalyzeSLBTool.get_slb_models(result)

            if page * settings.ALIYUN_PAGESIZE > results.get('TotalCount'):
                break

