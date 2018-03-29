# -*- coding:utf-8 -*-
# !/usr/bin/env python
# Time 18-3-28
# Author Yo
# Email YoLoveLife@outlook.com
from channels.routing import route
from ops import consumers
ops_routing = [
    consumers.MetaConsumer.as_route(path=r'^/ansible/(?P<meta>[0-9]+)/$'),
]