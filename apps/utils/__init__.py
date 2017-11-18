# -*- coding:utf-8 -*-
# !/usr/bin/env python
# Author Yo
# Email YoLoveLife@outlook.com
import json
FTP='192.168.254.134'
CHECKSUM=1

from datetime import datetime
import json
def toJSON(self):
    fields=[]
    for field in self._meta.fields:
        fields.append(field.name)
    d={}
    for attr in fields:
        if isinstance(getattr(self,attr), datetime):
            d[attr]=getattr(self, attr).__str__()
        else:
            d[attr]=getattr(self, attr)
    return json.dumps(d)

def str2dict(data):
    return json.loads(data)


class JstackThread():
    thread_name=""
    prio=0 #线程优先度
    osprio=0 #系统线程优先度
    tid=0 #系统线程对应
    nid=0 #系统线程对应
    stack_top="" #栈顶方法
    thread_status="NULL"
    position=""
