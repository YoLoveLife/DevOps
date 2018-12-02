# -*- coding:utf-8 -*-
# !/usr/bin/env python
# Time 18-7-2
# Author Yo
import datetime
from deveops.tools.aliyun_v2.analyze.base import AnalyzeTool
from django.conf import settings

class AnalyzeRDSTool(AnalyzeTool):

    @staticmethod
    def get_expired_day(time):
        expired = datetime.datetime.strptime(time, '%Y-%m-%dT%H:%M:%SZ')
        return (expired-datetime.datetime.now()).days

    @staticmethod
    def get_rds_expired_models(json_results):
        return {
            'expired': AnalyzeRDSTool.get_expired_day(json_results.get('ExpireTime')),
            'recognition_id': json_results.get('DBInstanceId'),
            'instancename': json_results.get('DBInstanceDescription'),
            'version': json_results.get('EngineVersion'),
            'readonly': len(json_results['ReadOnlyDBInstanceIds']['ReadOnlyDBInstanceId']),
            'status': 'Running'
        }

    @staticmethod
    def get_rds_models(json_results):
        return {
            'port': 3306,
            'name': json_results.get('DBInstanceDescription'),
        }