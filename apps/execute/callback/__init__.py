# -*- coding:utf-8 -*-
# !/usr/bin/env python
# Author Yo
# Email YoLoveLife@outlook.com

from ansible.plugins.callback import CallbackBase
from execute.models import Callback
import json

class ResultCallback(CallbackBase):
    '''
        解析callback返回的result内容
    '''
    def __init__(self):
        self.status=0
        self.c = Callback()

    #OK信息返回
    def v2_runner_on_ok(self, result, **kwargs):
        self.status = 1
        self.c.info = result._result['stdout']
        self.result = result._result['stdout_lines']
        self.c.save()
        return super(ResultCallback,self).v2_runner_on_ok(result,**kwargs)

    #失败
    def v2_runner_on_failed(self, result,ignore_errors=False):
        self.status=-1
        self.c.info = result._result['msg']
        self.result = result._result['msg']
        self.c.save()
        return super(ResultCallback,self).v2_runner_on_failed(result,ignore_errors)

    #目标不可达
    def v2_runner_on_unreachable(self, result):
        self.status = 0
        self.c.info = result._result['msg']
        self.result = result._result['msg']
        self.c.save()
        return super(ResultCallback,self).v2_runner_on_unreachable(result)

    def ResultExtract(self):
        return self.result