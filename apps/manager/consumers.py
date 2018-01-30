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
from django.conf import settings
from deveops.utils import aes

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
    def catch_redis_instance(self):
        return redis.StrictRedis()



class ManagerConsumer(YoSheelConsumer):

    def before_connect(self,**kwargs):
        host = Host.objects.filter(id=int(kwargs['pk'])).get()
        self.target = host.catch_ssh_connect
        return

    def connect(self, message, **kwargs):
        #Catch Info
        #DEMO
        try:
            result = self.before_connect(**kwargs)
        except socket.timeout:
            self.message.reply_channel.send(
                {"text": '\033[1;3;31m连接服务器超时\033[0m'},immediately=True)
            self.message.reply_channel.send({"accept": False})
            return
        except Exception,ex:
            self.message.reply_channel.send(
                {"text": '\033[1;3;31m连接服务器失败\033[0m'},
                immediately=True)
            self.message.reply_channel.send({"accept": False})
            return
        if result == 1:
            chan = self.target.invoke_shell(height=int(kwargs['rows']),width=int(kwargs['cols']))
            # chan.send('export JAVA_HOME=/usr/local/java')
            threadSend = YoShellSendThread(self.message,chan,self.catch_redis_instance())
            threadSend.setDaemon = True
            threadSend.start()

            theadRecv = YoShellRecvThread(self.message.reply_channel.name,chan)
            theadRecv.setDaemon = True
            theadRecv.start()
            self.message.reply_channel.send({"accept": True})
        else:
            self.message.reply_channel.send({"accept": False})

    def receive(self, text=None, bytes=None, **kwargs):
        #将用户的输入直接发送到redis的订阅者队列当中
        if text is not None:
            self.push_mission(self.message.reply_channel.name,text)

    def disconnect(self, message, **kwargs):
        # print('kkkr')
        self.jumper.close()
        self.target.close()