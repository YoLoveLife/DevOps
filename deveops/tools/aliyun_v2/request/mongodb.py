# -*- coding:utf-8 -*-
# !/usr/bin/env python
# Time 18-9-14
# Author Yo
from deveops.tools.aliyun_v2.request.base import AliyunTool
from deveops.tools.aliyun_v2.analyze.mongodb import AnalyzeMongoDBTool
from django.conf import settings


class AliyunMongoDBTool(AliyunTool):
    def init_action(self):
        self.request.set_domain('mongodb.aliyuncs.com')
        self.request.set_method('POST')
        self.request.set_version('2015-12-01')

    def action_get_instance(self):
        self.init()
        self.request.set_action_name('DescribeDBInstances')


    def tool_get_instances_models(self):
        self.action_get_instance()
        for page in range(1, 9999):
            self.request.add_query_param('PageNumber', page)
            self.request.add_query_param('PageSize', settings.ALIYUN_PAGESIZE)
            results = self.post()

            for result in results.get('DBInstances').get('DBInstance'):
                yield AnalyzeMongoDBTool.get_models(result)

            if page * settings.ALIYUN_PAGESIZE > results.get('TotalRecordCount'):
                break

    def tool_get_instance_models(self, instance_id):
        self.action_get_instance()
        self.request.add_query_param('DBInstanceIds',instance_id)
        results = self.post()
        yield AnalyzeMongoDBTool.get_models(results.get('DBInstances').get('DBInstance')[0])


    def tool_get_instances_expired_models(self):
        self.action_get_instance()
        for page in range(1, 9999):
            self.request.add_query_param('PageNumber', page)
            self.request.add_query_param('PageSize', settings.ALIYUN_PAGESIZE)
            results = self.post()

            for result in results.get('DBInstances').get('DBInstance'):
                yield AnalyzeMongoDBTool.get_expired_models(result)

            if page * settings.ALIYUN_PAGESIZE > results.get('TotalRecordCount'):
                break


    def tool_get_instance_expired_models(self, instance_id):
        self.action_get_instance()
        self.request.add_query_param('DBInstanceId', instance_id)
        results = self.post()
        yield AnalyzeMongoDBTool.get_expired_models(results.get('DBInstances').get('DBInstance')[0])
