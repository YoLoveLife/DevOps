# -*- coding:utf-8 -*-
# !/usr/bin/env python
# Time 18-9-14
# Author Yo
from deveops.tools.aliyun_v2.request.base import AliyunTool
from deveops.tools.aliyun_v2.analyze.vpc import AnalyzeVPCTool
from django.conf import settings


class AliyunVPCTool(AliyunTool):
    def init_action(self):
        self.request.set_domain('vpc.aliyuncs.com')
        self.request.set_method('POST')
        self.request.set_version('2016-04-28')


    def action_get_vpc(self):
        self.init()
        self.request.set_action_name('DescribeVpcs')


    def action_get_gateway(self):
        self.init()
        self.request.set_action_name('DescribeNatGateways')


    def action_get_dnat(self):
        self.init()
        self.request.set_action_name('DescribeForwardTableEntries')

    def action_get_snat(self):
        self.init()
        self.request.set_action_name('DescribeSnatTableEntries')


    def tool_get_vpcs(self):
        self.action_get_vpc()
        for page in range(1, 9999):
            self.request.add_query_param('PageNumber', page)
            self.request.add_query_param('PageSize', settings.ALIYUN_PAGESIZE)
            results = self.post()

            for result in results.get('Vpcs').get('Vpc'):
                yield AnalyzeVPCTool.get_vpc_models(result)

            if page * settings.ALIYUN_PAGESIZE > results.get('TotalCount'):
                break


    def tool_get_gateways(self):
        self.action_get_gateway()
        for page in range(1, 9999):
            self.request.add_query_param('PageNumber', page)
            self.request.add_query_param('PageSize', settings.ALIYUN_PAGESIZE)
            results = self.post()

            for result in results.get('NatGateways').get('NatGateway'):
                yield AnalyzeVPCTool.get_gateway_models(result)

            if page * settings.ALIYUN_PAGESIZE > results.get('TotalCount'):
                break

    def tool_get_gateways_byvpc(self, vpc_id):
        self.action_get_gateway()
        self.request.add_query_param('VpcId', vpc_id)
        results = self.post()
        yield AnalyzeVPCTool.get_gateway_models(results.get('NatGateways').get('NatGateway')[0])


    def tool_get_dnat(self, dnat_id):
        self.action_get_dnat()
        self.request.add_query_param('ForwardTableId', dnat_id)
        results = self.post()
        for result in results:
            yield AnalyzeVPCTool.get_dnat_models(result)


    def tool_get_snat(self, snat_id):
        self.action_get_snat()
        self.request.add_query_param('SnatTableId', snat_id)
        results = self.post()
        for result in results:
            yield AnalyzeVPCTool.get_snat_models(result)

