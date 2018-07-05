# -*- coding:utf-8 -*-
# !/usr/bin/env python
# Time 18-3-19
# Author Yo
# Email YoLoveLife@outlook.com
from .. import models, serializers
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated,AllowAny
from rest_framework.views import Response, status
from deveops.api import WebTokenAuthentication
import redis
from django.conf import settings
__all__ = [
    'ManagerDashboardAPI'
]

class ManagerDashboardAPI(WebTokenAuthentication,generics.ListAPIView):
    permission_classes = [IsAuthenticated,]
    # def get(self, request, *args, **kwargs):

    def get(self, request, *args, **kwargs):
        connect = redis.StrictRedis(host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=settings.REDIS_SPACE,
                                    password=settings.REDIS_PASSWD)
        return Response(connect.hgetall('MANAGER_STATUS'),status.HTTP_200_OK)
