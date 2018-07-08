# -*- coding:utf-8 -*-
# !/usr/bin/env python
# Time 17-11-16
# Author Yo
# Email YoLoveLife@outlook.com
from timeline.models import History
def decorator_api(timeline_type,):
    def wrapper(func):
        def inner_wrapper(*args, **kwargs):
            request, is_validated= func(*args, **kwargs)
            history = History(type=timeline_type, )
            history.is_validated = is_validated
            history.info = request.data
            history.save()
            return is_validated #DOT TOUCH it's magic
        return inner_wrapper
    return wrapper