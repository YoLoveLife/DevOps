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
        # target = paramiko.SSHClient()

        #DEMO
        self.target.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.target.connect('114.55.126.93', username='root', key_filename='/root/.ssh/id_rsa', port=52000)
        targettransport = self.target.get_transport()
        dest_addr = ('10.101.30.188', 22)
        local_addr = ('114.55.126.93', 52000)
        targetchannel = targettransport.open_channel("direct-tcpip", dest_addr, local_addr)

        self.jumper.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.jumper.connect('10.101.30.188', username='root', key_filename='/root/.ssh/id_rsa', sock=targetchannel,port=22)
        print(self.jumper,'connect')
        self.message.reply_channel.send({"accept": True})

    def receive(self, text=None, bytes=None, **kwargs):
        (stdin, stdout, stderr) = self.jumper.exec_command(text)
        print(self.jumper,'recevie')
        self.send(text=stdout.read(), bytes=bytes)

    def disconnect(self, message, **kwargs):
        self.jumper.close()
        self.target.close()