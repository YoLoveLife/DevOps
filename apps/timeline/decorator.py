# -*- coding:utf-8 -*-
# !/usr/bin/env python
# Time 17-11-16
# Author Yo
# Email YoLoveLife@outlook.com
from timeline.models import History
from django.conf import settings


def decorator_api(timeline_type,):
    def wrapper(func):
        def inner_wrapper(*args, **kwargs):
            msg, response = func(*args, **kwargs)
            if 100< response.status_code <300: # 200成功
                history = History(type=timeline_type, msg=msg)
                history.save()
            return response #DOT TOUCH it's magic
        return inner_wrapper
    return wrapper

#
# def decorator_api(timeline_type,):
#     def wrapper(func):
#         def inner_wrapper(*args, **kwargs):
#             request, is_validated= func(*args, **kwargs)
#             # history = History(type=timeline_type, )
#             # history.is_validated = is_validated
#             # history.info = request.data
#             # history.save()
#             return is_validated #DOT TOUCH it's magic
#         return inner_wrapper
#     return wrapper


def decorator_task(timeline_type,):
    def wrapper(func):
        def inner_wrapper(*args, **kwargs):
            results = func(*args, **kwargs)
            history = History(type=timeline_type, )
            history.is_validated = True
            history.save()
            return None  # DOT TOUCH it's magic
        return inner_wrapper
    return wrapper

