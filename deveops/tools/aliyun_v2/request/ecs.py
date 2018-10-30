# -*- coding:utf-8 -*-
# !/usr/bin/env python
# Time 18-9-14
# Author Yo
from deveops.tools.aliyun_v2.request.base import AliyunTool
from deveops.tools.aliyun_v2.analyze.ecs import AnalyzeECSTool
from django.conf import settings


class AliyunECSTool(AliyunTool):
    def init_action(self):
        self.request.set_domain('ecs.aliyuncs.com')
        self.request.set_method('POST')
        self.request.set_version('2014-05-26')

    def action_get_instance(self):
        self.init()
        self.request.set_action_name('DescribeInstances')

    def tool_get_instances_models(self):
        self.action_get_instance()
        for page in range(1, 9999):
            self.request.add_query_param('PageNumber', page)
            self.request.add_query_param('PageSize', settings.ALIYUN_PAGESIZE)
            results = self.post()
            for result in results.get('Instances').get('Instance'):
                yield AnalyzeECSTool.get_models(result)

            if page * settings.ALIYUN_PAGESIZE > results.get('TotalCount'):
                break


    def tool_get_instances_expired_models(self):
        self.action_get_instance()
        for page in range(1, 9999):
            self.request.add_query_param('PageNumber', page)
            self.request.add_query_param('PageSize', settings.ALIYUN_PAGESIZE)
            results = self.post()
            for result in results.get('Instances').get('Instance'):
                yield AnalyzeECSTool.get_expired_models(result)

            if page * settings.ALIYUN_PAGESIZE > results.get('TotalCount'):
                break

    def tool_get_instance_expired_models(self, instance_id):
        self.action_get_instance()
        self.request.add_query_param(
            'InstanceIds', '["{INSTANCE_ID}"]'.format(
                INSTANCE_ID=instance_id
            )
        )
        results = self.post()
        yield AnalyzeECSTool.get_expired_models(results.get('Instances').get('Instance')[0])


    def tool_get_instance_models(self, instance_id):
        self.action_get_instance()
        self.request.add_query_param(
            'InstanceIds', '["{INSTANCE_ID}"]'.format(
                INSTANCE_ID=instance_id
            )
        )
        results = self.post()
        try:
            yield AnalyzeECSTool.get_models(results.get('Instances').get('Instance')[0])
        except IndexError as e:
            yield 'delete'