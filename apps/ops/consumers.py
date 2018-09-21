# -*- coding:utf-8 -*-
# !/usr/bin/env python
# Time 18-3-28
# Author Yo
# Email YoLoveLife@outlook.com
from __future__ import absolute_import, unicode_literals
from channels.generic.websocket import WebsocketConsumer
from ops.tasks import ops_runner

__all__ = [
    "MetaConsumer"
]

class MetaConsumer(WebsocketConsumer):
    def websocket_receive(self, message):
        pass

    def websocket_disconnect(self, message):
        self.close()

    def websocket_connect(self, message):
        # 接受
        print('websocket')
        self.accept()
        # uuid = self.scope['url_route']['kwargs']['work']
        # ops_runner.delay(uuid, self)