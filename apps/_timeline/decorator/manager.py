# -*- coding:utf-8 -*-
# !/usr/bin/env python
# Time 17-11-16
# Author Yo
# Email YoLoveLife@outlook.com
from timeline.models import History
def decorator_manager(asset_id,api_name):
    def wrapper(func):
        def inner_wrapper(*args,**kwargs):
            his = History(type=asset_id, info=api_name, status=0)
            his.save()

            user,response = func(*args,**kwargs)

            his.user = user
            his.status = 1
            his.save()
            return response #别碰 这是魔法 DOT TOUCH it's magic
        return inner_wrapper
    return wrapper