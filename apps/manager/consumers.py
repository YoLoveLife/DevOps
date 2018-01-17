# -*- coding:utf-8 -*-
# !/usr/bin/env python
# Time 18-1-11
# Author Yo
# Email YoLoveLife@outlook.com
from __future__ import absolute_import,unicode_literals
from channels.handler import AsgiHandler
from channels.generic.websockets import WebsocketConsumer
import paramiko
import redis,socket,json
from manager.interactive import YoShellSendThread,YoShellRecvThread
from manager.models import Host,Group

class YoSheelConsumer(WebsocketConsumer):
    http_user = True
    http_user_and_session = True
    channel_session = True
    channel_session_user = True
    target = paramiko.SSHClient()
    jumper = paramiko.SSHClient()
    #以replay_name作为key 推送redis任务
    def push_mission(self,replay_name,msg):
        return redis.StrictRedis().publish(replay_name,msg)
        self.catch_redis().publish()

    #获取redis 获取信息链接
    def catch_redis_pubsub(self):
        return redis.StrictRedis().pubsub()

    #获取交互式的Shell
    def catch_chan(self,**kwargs):
        return self.target.invoke_shell(height=int(kwargs['rows']),width=int(kwargs['cols']))



class ManagerConsumer(YoSheelConsumer):

    def connect(self, message, **kwargs):
        #DEMO
        try:
            self.jumper.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            self.jumper.connect('114.55.126.93', username='root', key_filename='/root/.ssh/id_rsa', port=52000)
            jumpertransport = self.jumper.get_transport()
            dest_addr = ('10.101.30.188', 22)
            local_addr = ('114.55.126.93', 52000)
            jumperchannel = jumpertransport.open_channel("direct-tcpip", dest_addr, local_addr)
            self.target.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            self.target.connect('10.101.30.188', username='root', key_filename='/root/.ssh/id_rsa', sock=jumperchannel,port=22)
        except socket.timeout:
            self.message.reply_channel.send(
                {"text": json.dumps(['stdout', '\033[1;3;31m连接服务器超时\033[0m'])}, immediately=True)
            self.message.reply_channel.send({"accept": False})
            return
        except Exception,ex:
            self.message.reply_channel.send(
                {"text": json.dumps(['stdout', '\033[1;3;31m连接服务器失败\033[0m'.format(ex=str(ex))])},
                immediately=True)
            self.message.reply_channel.send({"accept": False})
            return

        threadSend = YoShellSendThread(self.message,self.catch_chan(**kwargs),self.catch_redis_pubsub())
        threadSend.setDaemon = True
        threadSend.start()

        theadRecv = YoShellRecvThread(self.message.reply_channel.name,self.catch_chan(**kwargs))
        theadRecv.setDaemon = True
        theadRecv.start()
        self.message.reply_channel.send({"accept": True})

    def receive(self, text=None, bytes=None, **kwargs):

        #将用户的输入直接发送到redis的订阅者队列当中
        if text is not None:
            if text == '\t':
                print('1')
            else:
                print('0')
            self.push_mission('112',text)
            print(self.message.reply_channel.name)

    def disconnect(self, message, **kwargs):
        print('kkkr')
        self.jumper.close()
        self.target.close()