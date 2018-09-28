# -*- coding:utf-8 -*-
# !/usr/bin/env python
# Time 18-3-28
# Author Yo
# Email YoLoveLife@outlook.com
from __future__ import absolute_import, unicode_literals
import json
from channels.generic.websocket import AsyncWebsocketConsumer
from ops.tasks import ops_runner

__all__ = [
    "MetaConsumer"
]

class MetaConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.work = str(self.scope['url_route']['kwargs']['work'])

        await self.channel_layer.group_add(str(self.work), self.channel_name)

        await self.accept()

        ops_runner.delay(self.work)


    async def receive(self, text_data):
        await self.channel_layer.group_send(
            self.work,
            ''
        )

    async def disconnect(self, code):
        await self.channel_layer.group_discard(
            self.work,
            self.channel_name
        )

    async def chat_message(self, event):
        message = event['message']
        await self.send(text_data=message)