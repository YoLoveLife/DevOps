# -*- coding:utf-8 -*-
# !/usr/bin/env python
# Time 18-7-3
# Author Yo
# Email YoLoveLife@outlook.com
import os
import django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "deveops.settings")
django.setup()

import json, datetime
from aliyunsdkcore import client
from aliyunsdkcore.request import CommonRequest
from django.conf import settings

class AliyunCDNTool(object):
    def __init__(self):
        self.clt = client.AcsClient(settings.ALIYUN_ACCESSKEY, settings.ALIYUN_ACCESSSECRET, 'cn-hangzhou')
        self.request = CommonRequest()
        AliyunCDNTool.request_to_json(self)

    def check(self, url):
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

    @staticmethod
    def get_json_results(results):
        return json.loads(results.decode('utf-8'))

    @staticmethod
    def request_to_json(obj):
        return obj.request.set_accept_format('json')

    def request_to_cdn(self, domain):
        self.request.set_domain('cdn.aliyuncs.com')
        self.request.set_method('POST')
        self.request.set_version('2014-11-11')
        self.request.set_action_name('RefreshObjectCaches')
        self.request.add_query_param('ObjectPath', domain)

        if self.check(domain) == 'FILE':
            self.request.add_query_param('ObjectType', 'File')
        else:
            self.request.add_query_param('ObjectType', 'Directory')

        try:
            response = self.clt.do_action_with_exception(self.request)
        except Exception as e:
            print(e)
            return {}
        return self.get_json_results(response)

    @staticmethod
    def request_to_result(result):
        print(result)
