# -*- coding:utf-8 -*-
# !/usr/bin/env python
# Time 18-1-11
# Author Yo
# Email YoLoveLife@outlook.com
from __future__ import absolute_import,unicode_literals
import os
from manager.urls.socket_urls import manager_routing
from ops.urls.socket_urls import ops_routing
# from channels import include

# os.environ.setdefault("DJANGO_SETTINGS_MODULE", "deveops.settings")    #这里填的是你的配置文件settings.py的位置
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack,SessionMiddleware

application = ProtocolTypeRouter({
    # '巍峨比赛噢参': AuthMiddlewareStack(
    #     URLRouter(
    #         manager_routing
    #     )
    # ),
    'websocket': SessionMiddleware(
        URLRouter(
            ops_routing
        )
    )
})

# routing = [
#     #route("http.request", consumers.http_consumer), 这个表项比较特殊，他响应的是http.request，也就是说有HTTP请求时就会响应，同时urls.py里面的表单会失效
#     include(manager_routing, path=r'^/manager'),
#     include(ops_routing, path=r'^/ops'),
# ]