# -*- coding:utf-8 -*-
# !/usr/bin/env python
# Time 18-1-11
# Author Yo
# Email YoLoveLife@outlook.com
# from channels.routing import route
from manager import consumers
from django.conf.urls import url
# manager_routing = [
#     consumers.ManagerConsumer.as_route(path=r'^/(?P<pk>[0-9]+)/wds/(?P<cols>[0-9]+)/(?P<rows>[0-9]+)/$'),
# ]

manager_routing = [
    url(r'^/(?P<pk>[0-9]+)/wds/(?P<cols>[0-9]+)/(?P<rows>[0-9]+)/$', consumers.ManagerConsumer)
]