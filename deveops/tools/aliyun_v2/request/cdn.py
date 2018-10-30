# -*- coding:utf-8 -*-
# !/usr/bin/env python
# Time 18-9-14
# Author Yo
from deveops.tools.aliyun_v2.request.base import AliyunTool
from deveops.tools.aliyun_v2.analyze.cdn import AnalyzeCDNTool
from django.conf import settings


class AliyunCDNTool(AliyunTool):
    def init_action(self):
        self.request.set_domain('cdn.aliyuncs.com')
        self.request.set_method('POST')
        self.request.set_version('2014-11-11')

    @staticmethod
    def check(url):
        if 'http' in url:
            index = url.find('//')
            header = url.find('/', index + 2)
            if '.' in url[header + 1:]: # uri
                return 'FILE'
            else:
                return 'DIR'
        else:
            index = url.find('/')
            if '.' in url[index+1:]:
                return 'FILE'
            else:
                return 'DIR'

    def action_refresh_cdn(self):
        self.init()
        self.request.set_action_name('RefreshObjectCaches')

    def action_get_cdn_task(self):
        self.init()
        self.request.set_action_name('DescribeRefreshTasks')

    def tool_flush_cdn(self, domain):
        self.action_refresh_cdn()
        self.request.add_query_param('ObjectPath', domain)

        if AliyunCDNTool.check(domain) == 'FILE':
            self.request.add_query_param('ObjectType', 'File')
        else:
            self.request.add_query_param('ObjectType', 'Directory')

        results = self.post()
        return results


    def tool_get_task(self, task_id):
        self.action_get_cdn_task()
        self.request.add_query_param('TaskId', task_id)
        results = self.post()
        yield AnalyzeCDNTool.get_models(results.get('Tasks').get('CDNTask')[0])


# 3145186050

