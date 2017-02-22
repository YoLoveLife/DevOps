# -*- coding:utf-8 -*-
# !/usr/bin/env python
# Author Yo
# Email YoLoveLife@outlook.com

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