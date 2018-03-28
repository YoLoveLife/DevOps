# -*- coding:utf-8 -*-
# !/usr/bin/env python
# Time 18-3-28
# Author Yo
# Email YoLoveLife@outlook.com
from __future__ import absolute_import, unicode_literals
from channels.generic.websockets import WebsocketConsumer
import redis
from ops.models import META

__all__ = [
    "YoShellConsumer"
]

class YoShellConsumer(WebsocketConsumer):
    http_user = True
    http_user_and_session = True
    channel_session = True
    channel_session_user = True

    # 获取redis 获取信息链接
    @staticmethod
    def catch_redis_instance(self):
        return redis.StrictRedis()


class MetaConsumer(YoShellConsumer):

    # 發起Ansible操作
    def before_connect(self,**kwargs):
        meta = META.objects.filter(id=int(kwargs['meta'])).get()
        play_source = meta.to_yaml
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
            threadSend = YoShellSendThread(self.message,chan,self.catch_redis_instance())
            threadSend.setDaemon = True
            threadSend.start()

            theadRecv = YoShellRecvThread(self.message.reply_channel.name,chan)
            theadRecv.setDaemon = True
            theadRecv.start()
            self.message.reply_channel.send({"accept": True})


    def receive(self, text=None, bytes=None, **kwargs):
        # 忽略用戶所有輸入內容
        pass

    def disconnect(self, message, **kwargs):
        self.message.reply_channel.send(
            {"text": '\033[1;3;31m' + u'您的连接已结束 如果不是您主动释放连接 则相关资产信息有误' + '\033[0m'}, immediately=True)
        self.message.reply_channel.send({"accept": False})
        self.jumper.close()
        self.target.close()