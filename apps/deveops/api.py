# -*- coding:utf-8 -*-
# !/usr/bin/env python
# Time 18-3-21
# Author Yo
# Email YoLoveLife@outlook.com
from rest_framework.renderers import JSONRenderer
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

__all__ = [
    'WebTokenAuthentication'
]


class WebTokenAuthentication():
    # authentication_classes = (JSONWebTokenAuthentication,)
    # renderer_classes = (JSONRenderer ,)
    ddr = 1