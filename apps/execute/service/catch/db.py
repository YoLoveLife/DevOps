# -*- coding:utf-8 -*-
# !/usr/bin/env python
# Time 17-10-9
# Author Yo
# Email YoLoveLife@outlook.com
from execute.service import AnsibleService
from execute.callback import ResultCallback
from execute.models import Callback
from inventory.maker import Maker
__metaclass__ = type
class DBAnsibleService(AnsibleService):
    def __init__(self,hostlist):
        self.maker = Maker()
        self.maker.inventory_maker(hostlist)
        super(DBAnsibleService,self).__init__(self.maker.filename)

    def run(self,db,tasklist):
        callback = ResultCallback()
        self.push_callback(callback)

        super(DBAnsibleService,self).run(tasklist,self.maker)

        list = callback.ResultExtract()
        self.update(list,db)

    def update(self,list,db):
        detail = db.dbdetail.get()
        detail.com_insert = list[0].strip()
        detail.com_update = list[1].strip()
        detail.max_connections = list[2].strip()
        detail.thread_running = list[3].strip()
        detail.save()
