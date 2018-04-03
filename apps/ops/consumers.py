# -*- coding:utf-8 -*-
# !/usr/bin/env python
# Time 18-3-28
# Author Yo
# Email YoLoveLife@outlook.com
from __future__ import absolute_import, unicode_literals
from channels.generic.websockets import WebsocketConsumer
from django.core.exceptions import ObjectDoesNotExist
import redis
from ops.models import META
from ops.ansible import playbook
from ops.interactive import AnsibleRecvThread
__all__ = [
    "MetaConsumer"
]


class MetaConsumer(WebsocketConsumer):
    http_user = True
    http_user_and_session = True
    channel_session = True
    channel_session_user = True

    # 獲取要使用的Ansible內容
    def before_connect(self,**kwargs):
        meta = META.objects.filter(id=int(kwargs['meta'])).get()
        play_source = meta.to_yaml
        inventory = meta.group.users_list_byconnectip
        key = meta.group.key.private_key
        return play_source, inventory, key

    # 發起Ansible執行
    def connect(self, message, **kwargs):
        try:
            play_source, inventory, key = self.before_connect(**kwargs)
        except ObjectDoesNotExist:
            from deveops.asgi import channel_layer
            channel_layer.send(self.replay_name, {'text': u'您执行的任务缺少必要的密钥或者跳板机请联系管理员解决'})
            channel_layer.send(self.replay_name,{'close': True})
            return

        threadSend = AnsibleRecvThread(play_source, inventory, key, self.message.reply_channel.name)
        threadSend.setDaemon = True
        threadSend.start()


    def receive(self, text=None, bytes=None, **kwargs):
        # 忽略用戶所有輸入內容
        pass

    def disconnect(self, message, **kwargs):
        pass