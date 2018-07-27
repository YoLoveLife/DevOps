# -*- coding:utf-8 -*-
# !/usr/bin/env python
# Time 18-1-11
# Author Yo
# Email YoLoveLife@outlook.com
from __future__ import absolute_import,unicode_literals
from ops.urls.socket_urls import ops_routing
from console.urls.socket_urls import console_routing

# os.environ.setdefault("DJANGO_SETTINGS_MODULE", "deveops.settings")    #这里填的是你的配置文件settings.py的位置
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from deveops.channel_auth import TokenAuthMiddlewareStack

application = ProtocolTypeRouter({
    # '巍峨比赛噢参': AuthMiddlewareStack(
    #     URLRouter(
    #         manager_routing
    #     )
    # ),
    'websocket': TokenAuthMiddlewareStack(
        URLRouter(
            ops_routing,
        )
    ),
    'websocket': TokenAuthMiddlewareStack(
        URLRouter(
            console_routing,
        )
    )
})