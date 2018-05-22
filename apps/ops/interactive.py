# -*- coding:utf-8 -*-
# !/usr/bin/env python
# Time 18-1-16
# Author Yo
# Email YoLoveLife@outlook.com
from __future__ import absolute_import, unicode_literals
import threading
from ops.ansible import playbook
from django.conf import settings
__all__ = [
    "AnsibleRecvThread"
]


class AnsibleRecvThread(threading.Thread):
    CACHE = 1024

    def __init__(self, work, play_source, inventory, key, vars_dict, reply_channel_name):
        super(AnsibleRecvThread, self).__init__()
        self.reply_channel_name = reply_channel_name
        self.key = key
        self.vars_dict = vars_dict
        self.play_source = play_source
        self.inventory = inventory
        self.work = work

    def run(self):
        p = playbook.Playbook(self.vars_dict, self.inventory, self.reply_channel_name, self.key, self.work.push_mission)
        p.import_task(self.play_source)
        p.run()
        self.work.status = 3
        self.work.save()