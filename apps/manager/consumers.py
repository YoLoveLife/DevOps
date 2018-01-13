# -*- coding:utf-8 -*-
# !/usr/bin/env python
# Time 18-1-11
# Author Yo
# Email YoLoveLife@outlook.com
from channels.handler import AsgiHandler
from channels.generic.websockets import WebsocketConsumer
import paramiko
class ManagerConsumer(WebsocketConsumer):
    # http_user = True
    # http_user_and_session = True
    # channel_session = True
    # channel_session_user = True

    target = paramiko.SSHClient()
    jumper = paramiko.SSHClient()
    # def connection_groups(self, **kwargs):
    #     return ["test"]

    def connect(self, message, **kwargs):

        #DEMO
        self.jumper.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.jumper.connect('114.55.126.93', username='root', key_filename='/root/.ssh/id_rsa', port=52000)
        jumpertransport = self.jumper.get_transport()
        dest_addr = ('10.101.30.188', 22)
        local_addr = ('114.55.126.93', 52000)
        jumperchannel = jumpertransport.open_channel("direct-tcpip", dest_addr, local_addr)

        self.target.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.target.connect('10.101.30.188', username='root', key_filename='/root/.ssh/id_rsa', sock=jumperchannel,port=22)
        print(self.target,'connect')
        self.message.reply_channel.send({"accept": True})

    def receive(self, text=None, bytes=None, **kwargs):
        (stdin, stdout, stderr) = self.target.exec_command('hostname')
        print(self.target,'recevie')
        print(stdout.read())
        self.send(text=stdout.read(), bytes=bytes)

    def disconnect(self, message, **kwargs):
        self.jumper.close()
        self.target.close()