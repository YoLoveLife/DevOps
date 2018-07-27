# -*- coding:utf-8 -*-
# !/usr/bin/env python
# Time 18-7-27
# Author Yo
# Email YoLoveLife@outlook.com

from channels.auth import AuthMiddlewareStack
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import AnonymousUser
from django.db import close_old_connections

class TokenAuthMiddleware(object):
    def __init__(self, inner):
        self.inner = inner

    def __call__(self, scope):
        headers = dict(scope['headers'])
        print(123,headers)
        if b'authorization' in headers:
            try:
                token_name, token_key = headers[b'authorization'].decode().split()
                if token_name == 'Token':
                    token = Token.objects.get(key=token_key)
                    scope['user'] = token.user
                    close_old_connections()
            except Token.DoesNotExist:
                scope['user'] = AnonymousUser()
        return self.inner(scope)


TokenAuthMiddlewareStack = lambda inner: TokenAuthMiddleware(AuthMiddlewareStack(inner))