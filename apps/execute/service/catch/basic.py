# -*- coding:utf-8 -*-
from execute.service import AnsibleService
from execute.callback.catch import basic

class BasicAnsibleService(AnsibleService):

    def __init__(self,name):
        super(BasicAnsibleService,self).__init__(self,name)

    def run(self,hostlist,tasklist):
        self.push_callback(basic.BasicResultCallback())
        return super(BasicAnsibleService,self).run(hostlist,tasklist)


