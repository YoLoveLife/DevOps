# -*- coding:utf-8 -*-
# !/usr/bin/env python
# Time 18-7-2
# Author Yo
import datetime
from deveops.tools.aliyun_v2.analyze.base import AnalyzeTool
from django.conf import settings

class AnalyzeSLBTool(AnalyzeTool):
    @staticmethod
    def get_slb_models(result):
        try:
            return {
                'name': result.get('LoadBalancerName'),
                'uuid': result.get('LoadBalancerId'),
                'type': result.get('AddressType'),
            }
        except Exception as e:
            return AnalyzeTool.get_models(result)
