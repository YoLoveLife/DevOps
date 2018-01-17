# -*- coding:utf-8 -*-
# !/usr/bin/env python
# Time 18-1-16
# Author Yo
# Email YoLoveLife@outlook.com
from __future__ import absolute_import,unicode_literals
import socket,json,threading,ast,codecs
from paramiko.py3compat import u
from django.utils.encoding import smart_unicode
# def linux_shell(chan):
#     import select
#     pass

class YoShellRecvThread(threading.Thread):
    CACHE = 1024
    def __init__(self,channel,chan):
        super(YoShellRecvThread, self).__init__()
        self.chan = chan
        self.channel = channel
        self.count = 0

    def run(self):
        while(True):
            try:
                stdout = list()
                msg = u(self.chan.recv(self.CACHE))
                from deveops.asgi import channel_layer  # 为什么一定要在函数中引入才可以？

                if len(msg) == 0:
                    channel_layer.send(self.channel, {
                        'text': json.dumps(smart_unicode('\r\n*** EOF\r\n'))})
                    break
                if msg == "exit\r\n" or msg == "logout\r\n" or msg == 'logout': #如果exit则返回
                    self.chan.close()
                else:
                    stdout.append([codecs.getincrementaldecoder('UTF-8')('replace').decode(msg)])
                channel_layer.send(self.channel, {'text': json.dumps(smart_unicode(msg)) })
            except socket.timeout:
                pass
            except Exception,e:
                pass

class YoShellSendThread(threading.Thread):
    def __init__(self,message,chan,pubsub):
        super(YoShellSendThread, self).__init__()
        self._stop_event = threading.Event()
        self.message = message
        self.chan = chan
        self.pubsub = self.catch_pubsub(pubsub)
        self.count = 1

    def catch_pubsub(self,pubsub):
        import redis
        redis_instance = redis.StrictRedis()
        redis_sub = redis_instance.pubsub()
        redis_sub.subscribe('112')
        return redis_sub

    def stop(self):
        self._stop_event.set()

    def run(self):#持续获取队列中传递进来的用户命令并直接传递到远程的服务器
        for item in self.pubsub.listen():
            if item['type'] == 'message':
                self.chan.send(item['data'])

        # while True:
        #     msg = self.pubsub.get_message()
        #     if msg is not None:
        #         print(msg)
        #         if isinstance(msg['data'],(str,basestring,unicode)):
        #             try:
        #                 data = ast.literal_eval(msg['data'])
        #             except Exception:
        #                 data = msg['data']
        #         else:
        #             data = msg['data']
        #
        #         try:
        #             self.chan.send(str(data))
        #         except socket.error:
        #             self.stop()

