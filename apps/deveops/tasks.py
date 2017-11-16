# -*- coding:utf-8 -*-
# !/usr/bin/env python
# Time 17-11-15
# Author Yo
# Email YoLoveLife@outlook.com

def PingOnlineTask():
    # BaseTask.PingOnlineService()
    from manager.models import Host
    import time
    host = Host.objects.all()[0]
    host.info = str(time.time())
    host.save()