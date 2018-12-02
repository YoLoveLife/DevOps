# -*- coding:utf-8 -*-
# !/usr/bin/env python
# Time 18-7-2
# Author Yo
import datetime
from deveops.tools.aliyun_v2.analyze.base import AnalyzeTool
from django.conf import settings

class AnalyzeVPCTool(AnalyzeTool):
    @staticmethod
    def get_vpc_models(result):
        try:
            return {
                'vpc_name': result.get('VpcName'),
                'vpc_desc': result.get('Description'),
                'gateway': result.get('NatGatewayIds').get('NatGatewayIds')[0],
                'switch': result.get('VSwitchIds').get('VSwitchIds')[0],
                'router': result.get('VRouterId')
            }
        except Exception as e:
            return AnalyzeTool.get_models(result)


    @staticmethod
    def get_gateway_models(result):
        try:
            return {
                'snat_id': result.get('ForwardTableIds').get('ForwardTableId'),
                'dnat_id': result.get('SnatTableIds').get('SnatTableId'),
                'desc': result.get('Description'),
                'name': result.get('Name'),
            }
        except Exception as e:
            return AnalyzeTool.get_models(result)

    @staticmethod
    def get_dnat_models(result):
        try:
            return {
                'exter_ip': result.get('ExternalIp'),
                'exter_port': result.get('ExternalPort'),
                'inter_ip': result.get('InternalIp'),
                'inter_port': result.get('InternalPort'),
            }
        except Exception as e:
            return AnalyzeTool.get_models(result)


    @staticmethod
    def get_snat_models(result):
        try:
            return {
                'snat_ip': result.get('SnatIp'),
            }
        except Exception as e:
            return AnalyzeTool.get_models(result)