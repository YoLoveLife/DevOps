# -*- coding:utf-8 -*-
# !/usr/bin/env python
# Author Yo
# Email YoLoveLife@outlook.com

from ansible.plugins.callback import CallbackBase
import json

class ResultCallback(CallbackBase):
    '''
        解析callback返回的result内容
    '''

    #OK信息返回
    def v2_runner_on_ok(self, result, **kwargs):
        """Print a json representation of the result
        This method could store the result in an instance attribute for retrieval later
        """
        # host = result._host
        #str="h:%s r:success module:%s arvg:%s" % (host,json.dumps(result._result['invocation']["module_name"]),json.dumps(result._result['invocation']["module_args"]))
        #print(str)
        #if json.dumps(result._result['invocation']['module_name'])=='yum':
        # print(json.dumps(result._result))
        return super(ResultCallback,self).v2_runner_on_ok(result,**kwargs)

    #失败
    def v2_runner_on_failed(self, result, ignore_errors=False):
        # host = result._host.get_name()
        #self.runner_on_failed(host, result._result, ignore_errors)
       # print("????")
       # print(json.dumps(result._result))
       # print("????")
       # str="h:%s r:failed module:%s arvg:%s"%(host,json.dumps(result._result['invocation']["module_name"]),json.dumps(result._result['invocation']["module_args"]))
       # print(str)
       #  print(json.dumps(result._result))
        return super(ResultCallback,self).v2_runner_on_failed(result,ignore_errors)
    #目标不可达
    def v2_runner_on_unreachable(self, result):
        # host = result._host.get_name()
        #self.runner_on_unreachable(host, result._result)
      #  str="h:%s r:unreach module:%s arvg:%s"%(host,json.dumps(result._result['invocation']["module_name"]),json.dumps(result._result['invocation']["module_args"]))
      #  print(str)
      #   print(json.dumps(result._result))
        return super(ResultCallback,self).v2_runner_on_unreachable(result)