# -*- coding:utf-8 -*-
# !/usr/bin/env python
# Time 18-3-28
# Author Yo
# Email YoLoveLife@outlook.com
from __future__ import absolute_import, unicode_literals
from channels.generic.websockets import WebsocketConsumer
from work.models import Code_Work
from django.conf import settings
from ops.interactive import AnsibleRecvThread
import time
import os,stat
__all__ = [
    "MetaConsumer"
]


class MetaConsumer(WebsocketConsumer):
    http_user = True
    http_user_and_session = True
    channel_session = True
    channel_session_user = True

    def write_key(self, key, file_path):
        try:
            f = open(file_path, 'w')
            f.write(key.private_key)
            f.close()
        except Exception:
            return '~/.ssh/id_rsa'
        os.chmod(file_path,stat.S_IWUSR|stat.S_IRUSR)
        return

    # 獲取要使用的Ansible內容
    def before_connect(self,**kwargs):
        # 查询必要数据
        work = Code_Work.objects.filter(id=int(kwargs['work'])).get()
        play_source = work.mission.to_yaml
        inventory = work.mission.group.users_list_byconnectip

        # 创建临时目录
        TMP = settings.OPS_ROOT+str(work.uuid)+'/'
        if not os.path.exists(TMP):
            os.makedirs(TMP)

        if work.mission.group.key is not None:
            self.write_key(work.mission.group.key, TMP+str(time.time())+'.key')
            return work, play_source, inventory, TMP+str(time.time())+'.key'
        else:
            return work, play_source, inventory, None

    # 發起Ansible執行
    def connect(self, message, **kwargs):
        from deveops.asgi import channel_layer
        work, play_source, inventory, key = self.before_connect(**kwargs)
        if key == None or len(play_source)==0:
            channel_layer.send(self.message.reply_channel.name, {'text': u'\r\n您执行的任务缺少必要的密钥或者跳板机请联系管理员解决'})
            channel_layer.send(self.message.reply_channel.name, {'close': True})
            return
        elif work.status == 3:
            channel_layer.send(self.message.reply_channel.name, {'text': u'\r\n当前工单已经执行完毕 如有需要请重新创建'})
            channel_layer.send(self.message.reply_channel.name, {'close': True})
            return

        threadSend = AnsibleRecvThread(work, play_source, inventory, key, self.message.reply_channel.name)
        threadSend.setDaemon = True
        threadSend.start()


    def receive(self, text=None, bytes=None, **kwargs):
        # 忽略用戶所有輸入內容
        pass

    def disconnect(self, message, **kwargs):
        pass