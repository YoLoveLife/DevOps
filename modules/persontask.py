# -*- coding:utf-8 -*-
# !/usr/bin/env python
# Author Yo
# Email YoLoveLife@outlook.com

class PersonTask():
    def __init__(self,module="shell",args="",register='shell_out'):
        self.module=module
        self.args=args
        self.register=register

    def push_task(self):
        return dict(action=dict(module=self.module,args=self.args),register=self.register)
