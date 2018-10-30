# -*- coding:utf-8 -*-
# !/usr/bin/env python
# Time 18-1-11
# Author Yo
# Email YoLoveLife@outlook.com
from __future__ import absolute_import,unicode_literals
from ops.urls.socket_urls import ops_routing
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack

application = ProtocolTypeRouter({
    'websocket': AuthMiddlewareStack(
        URLRouter(
            ops_routing,
        )
    )
})