# -*- coding:utf-8 -*-
# !/usr/bin/env python
# Time 18-7-2
# Author Yo
import os
import django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "deveops.settings")
django.setup()


from aliyunsdkcore import client
from django.conf import settings
from aliyunsdkcore.request import CommonRequest
from deveops.tools.aliyun_v2.analyze.base import AnalyzeTool

class AliyunTool(object):
    def __init__(self):
        self.clt = client.AcsClient(settings.ALIYUN_ACCESSKEY, settings.ALIYUN_ACCESSSECRET, 'cn-hangzhou')
        self.request = None

    def request_to_json(self):
        self.request.set_accept_format('json')

    def init_request(self):
        request = CommonRequest()
        self.request = request
        self.request_to_json()

    def init_action(self):
        pass


    def init(self):
        self.init_request()
        self.init_action()


    def post(self):
        try:
            response = self.clt.do_action_with_exception(self.request)
        except Exception as e:
            print(e)
            return {}
        return AnalyzeTool.results_to_json(response)
