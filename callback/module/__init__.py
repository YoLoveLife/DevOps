# -*- coding:utf-8 -*-
# !/usr/bin/python2.6
# Author Yo
# Email YoLoveLife@outlook.com
import json
class BaseModule():
    def result2Json(self,value):
        self._result=json.loads(value)

    def value2Args(self,*args,**kwargs):
        self._ansible_parsed=self._result['_ansible_parsed']
        self._changed=self._result['changed']
        self.__ansible_no_log=self._result['_ansible_no_log']

    def pop_task(self):
        pass

if __name__ == "__main__":
    ddr = {'rr':{'ddr':'zzc'}}
    ba=BaseModule()
    ba.result2Json(ddr)