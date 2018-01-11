# -*- coding:utf-8 -*-
# !/usr/bin/env python
# Time 18-1-11
# Author Yo
# Email YoLoveLife@outlook.com
from paramiko import SSHClient
from channels.handler import AsgiHandler
from channels.generic.websockets import WebsocketConsumer
class ManagerConsumer(WebsocketConsumer):

    http_user_and_session = True

    def connection_groups(self, **kwargs):
        return ["test"]

    def connect(self, message, **kwargs):
        print('connect')
        self.message.reply_channel.send({"accept": True})

    def receive(self, text=None, bytes=None, **kwargs):
        import os, commands
        (status, output) = commands.getstatusoutput(text)
        # list = output.split('\n')
        # print(list)
        # for i in list:
        self.send(text=u'1', bytes=bytes)
        self.send(text=u'2', bytes=bytes)
        self.send(text=u'3', bytes=bytes)

    def disconnect(self, message, **kwargs):
        print('disconnect')
        pass