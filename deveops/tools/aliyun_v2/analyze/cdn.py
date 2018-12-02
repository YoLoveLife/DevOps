# -*- coding:utf-8 -*-
# !/usr/bin/env python
# Time 18-7-2
# Author Yo
import datetime,json
from deveops.tools.aliyun_v2.analyze.base import AnalyzeTool
from django.conf import settings


class AnalyzeCDNTool(AnalyzeTool):

    @staticmethod
    def get_status(status):
        if status == 'Complete':
            return settings.STATUS_CDN_DONE
        elif status == 'Refreshing':
            return settings.STATUS_CDN_RUN
        elif status == 'Failed':
            return settings.STATUS_CDN_ERROR

    @staticmethod
    def get_models(result):
        return {
            'status': AnalyzeCDNTool.get_status(result.get('Status')),
            'process': float(result.get('Process')[:-1]),
        }