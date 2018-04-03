# -*- coding:utf-8 -*-
# !/usr/bin/env python
# Time 18-1-16
# Author Yo
# Email YoLoveLife@outlook.com
from __future__ import absolute_import, unicode_literals
import threading
from ops.ansible import playbook

__all__ = [
    "AnsibleRecvThread"
]


class AnsibleRecvThread(threading.Thread):
    CACHE = 1024

    def __init__(self,play_source, inventory, key, reply_channel_name):
        super(AnsibleRecvThread, self).__init__()
        self.reply_channel_name = reply_channel_name
        self.key = key
        self.play_source = play_source
        self.inventory = inventory

    def run(self):
        p = playbook.Playbook(self.inventory, self.reply_channel_name, self.key)
        p.import_task(self.play_source)
        p.run()
