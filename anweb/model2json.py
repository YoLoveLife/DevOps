# -*- coding:utf-8 -*-
# !/usr/bin/env python
# Time 17 17:18
# Author Yo
# Email YoLoveLife@outlook.com
from models import Group
from django.core import serializers
from util import toJSON
def host9hostsearch(data):
    data=eval(data)
    for i in data:
        print(i['fields'])
        print(i['fields']['group_id'])
        group=Group.objects.get(id=int(i['fields']['group_id']))
        print(toJSON(group))
