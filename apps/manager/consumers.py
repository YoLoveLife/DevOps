# -*- coding:utf-8 -*-
# !/usr/bin/env python
# Time 18-1-11
# Author Yo
# Email YoLoveLife@outlook.com
from __future__ import absolute_import, unicode_literals
from channels.generic.websocket import WebsocketConsumer
import paramiko
import redis
from manager.interactive import YoShellSendThread, YoShellRecvThread
from manager.models import Host, Group

__all__ = [
    "YoShellConsumer", "YoShellRecvThread", "YoShellSendThread"
]

class YoShellConsumer(WebsocketConsumer):
    http_user = True
    http_user_and_session = True
    channel_session = True
    channel_session_user = True
    target = paramiko.SSHClient()
    jumper = paramiko.SSHClient()
    # 以replay_name作为key 推送redis任务
    def push_mission(self,replay_name,msg):
        return redis.StrictRedis().publish(replay_name,msg)
        self.catch_redis().publish()

    # 获取redis 获取信息链接
    def catch_redis_instance(self):
        return redis.StrictRedis()


class ManagerConsumer(YoShellConsumer):

    def before_connect(self,**kwargs):
        host = Host.objects.filter(id=int(kwargs['pk'])).get()
        self.target = host.catch_ssh_connect.instance
        return host.catch_ssh_connect

    def connect(self, message, **kwargs):
        result = self.before_connect(**kwargs)
        if result.status == 0:
            self.message.reply_channel.send(
                {"text": '\033[1;3;31m'+result.last_result+'\033[0m'},immediately=True)
            self.message.reply_channel.send({"accept": False})
            return
        else:
            chan = self.target.invoke_shell(height=int(kwargs['rows']),width=int(kwargs['cols']))
            # chan.send('export JAVA_HOME=/usr/local/java')
            threadSend = YoShellSendThread(self.message,chan,self.catch_redis_instance())
            threadSend.setDaemon = True
            threadSend.start()

            theadRecv = YoShellRecvThread(self.message.reply_channel.name,chan)
            theadRecv.setDaemon = True
            theadRecv.start()
            self.message.reply_channel.send({"accept": True})


    def receive(self, text=None, bytes=None, **kwargs):
        # 将用户的输入直接发送到redis的订阅者队列当中
        if text is not None:
            self.push_mission(self.message.reply_channel.name,text)

    def disconnect(self, message, **kwargs):
        self.message.reply_channel.send(
            {"text": '\033[1;3;31m' + u'您的连接已结束 如果不是您主动释放连接 则相关资产信息有误' + '\033[0m'}, immediately=True)
        self.message.reply_channel.send({"accept": False})
        self.jumper.close()
        self.target.close()