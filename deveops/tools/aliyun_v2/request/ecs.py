# -*- coding:utf-8 -*-
# !/usr/bin/env python
# Time 18-9-14
# Author Yo
from deveops.tools.aliyun_v2.request.base import AliyunTool
from deveops.tools.aliyun_v2.analyze.ecs import AnalyzeECSTool
from django.conf import settings


class AliyunSecurityTool(AliyunTool):
    def init_action(self):
        self.request.set_domain('ecs.aliyuncs.com')
        self.request.set_method('POST')
        self.request.set_version('2014-05-26')

    def action_get_security_group(self):
        self.init()
        self.request.set_action_name('DescribeSecurityGroups')

    def action_authorize_egress(self):
        self.init()
        self.request.set_action_name('AuthorizeSecurityGroupEgress')

    def action_revoke_ingress(self):
        self.init()
        self.request.set_action_name('RevokeSecurityGroup')

    def action_revoke_egress(self):
        self.init()
        self.request.set_action_name('RevokeSecurityGroupEgress')

    def action_get_ingress(self):
        self.init()
        self.request.set_action_name('DescribeSecurityGroupAttribute')
        self.request.add_query_param('Direction', 'ingress')

    def tool_get_security_group_models(self):
        self.action_get_security_group()
        for page in range(1, 9999):
            self.request.add_query_param('PageNumber', page)
            self.request.add_query_param('PageSize', settings.ALIYUN_PAGESIZE)
            results = self.post()
            for result in results.get('SecurityGroups').get('SecurityGroup'):
                yield AnalyzeECSTool.get_security_models(result)

            if page * settings.ALIYUN_PAGESIZE > results.get('TotalCount'):
                break

    def tool_get_security_group_ingress_models(self, security_id):
        self.action_get_ingress()
        self.request.add_query_param('SecurityGroupId', security_id)
        results = self.post()
        return results

    def tool_revoke_ingress(self, *args, **kwargs):
        self.action_revoke_ingress()
        for arg in kwargs:
            self.request.add_query_param(
                arg, kwargs[arg]
            )
        return self.post()

    def tool_authorize_egress(self, *args, **kwargs):
        self.action_authorize_egress()
        for arg in kwargs:
            self.request.add_query_param(
                arg, kwargs[arg]
            )
        return self.post()

    def tool_revoke_egress(self, *args, **kwargs):
        self.action_revoke_egress()
        for arg in kwargs:
            self.request.add_query_param(
                arg, kwargs[arg]
            )
        return self.post()


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