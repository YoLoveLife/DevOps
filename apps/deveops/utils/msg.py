# -*- coding:utf-8 -*-
# !/usr/bin/env python
# Time 18-1-30
# Author Yo
# Email YoLoveLife@outlook.com

class Message(object):
    def __init__(self):
        self.status = 0
        self.results = []
        self.instance = None

    def get_status(self):
        if self.status == 1:
            return 'success'
        elif self.status == 0:
            return 'fail'
        else:
            return "unknow"

    @property
    def catch_msg(self):
        return self.results,self.instance

    def fuse_msg(self,status,result,instance):
        self.status = status
        self.results.append(result)
        self.instance=instance
        return self

    @property
    def last_result(self):
        return self.results[-1]

    def catch_instance(self):
        return self.instance

    def join_msg(self,msg):
        self.results = msg.results + self.results
        self.instance = msg.instance
        return self