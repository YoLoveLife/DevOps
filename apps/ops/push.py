# -*- coding:utf-8 -*-
# !/usr/bin/env python
# Time 18-4-11
# Author Yo
# Email YoLoveLife@outlook.com


import threading
from ops.models import Push_Mission

class PushingThread(threading.Thread):
    CACHE = 1024

    def __init__(self, push_id):
        super(PushingThread, self).__init__()
        # 创建临时执行目录
        push = Push_Mission.objects.filter(id=push_id).get()
        self.push = push


    def run(self):
        pass

