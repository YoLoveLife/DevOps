# -*- coding:utf-8 -*-
# !/usr/bin/env python
# Time 18-1-30
# Author Yo
# Email YoLoveLife@outlook.com

class Message(object):
    def __init__(self):
        self.results = []
        self.instance = None

    @property
    def catch_msg(self):
        return self.results,self.instance

    def fuse_msg(self,result,instance):
        self.results.append(result)
        self.instance=instance
        return self

    @property
    def last_result(self):
        return self.results[-1]

    def join_msg(self,msg):
        self.results = msg.results + self.results
        self.instance = msg.instance
        return self