# -*- coding:utf-8 -*-
# !/usr/bin/env python
# Time 17-10-9
# Author Yo
# Email YoLoveLife@outlook.com
from execute.service import AnsibleService
from execute.callback.catch import db
from execute.models import Callback
from inventory.maker import Maker
__metaclass__ = type
class DBAnsibleService(AnsibleService):
    def __init__(self,hostlist):
        self.maker = Maker()
        self.maker.inventory_maker(hostlist)
        super(DBAnsibleService,self).__init__(self.maker.filename)

    def run(self,hostlist,tasklist):
        callback = db.DBResultCallback()
        self.push_callback(callback)

        super(DBAnsibleService,self).run(tasklist,self.maker)

        list = callback.ResultExtract()
        self.update(list,hostlist)

    def update(self,list,hostlist):
        for host in hostlist:
            host.coreness = list[0]
            host.memory = list[1]
            host.root_disk = list[2]
            host.hostname = list[3]
            host.save()
