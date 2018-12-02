# -*- coding:utf-8 -*-
# !/usr/bin/env python
# Time 18-7-2
# Author Yo
import datetime
from deveops.tools.aliyun_v2.analyze.base import AnalyzeTool
from django.conf import settings

class AnalyzeKVStoreTool(AnalyzeTool):

    @staticmethod
    def get_expired_day(time):
        expired = datetime.datetime.strptime(time, '%Y-%m-%dT%H:%M:%SZ')
        return (expired-datetime.datetime.now()).days

    @staticmethod
    def get_expired_models(json_results):
        return {
            'expired': AnalyzeKVStoreTool.get_expired_day(json_results.get('EndTime')),
            'recognition_id': json_results.get('InstanceId'),
            'instancename': json_results.get('InstanceName'),
            'version': json_results.get('EngineVersion'),
            'connect_domain': json_results.get('ConnectionDomain'),
            'type': json_results.get('InstanceType'),
            'status': 'Running'
        }