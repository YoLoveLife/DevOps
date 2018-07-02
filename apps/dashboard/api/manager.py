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
import json
from django.conf import settings

__all__ = [
    "DashboardManagerAPI",
]


class DashboardManagerAPI(WebTokenAuthentication,generics.ListAPIView):
    permission_classes = [AllowAny,]
    # def get(self, request, *args, **kwargs):

    def get(self, request, *args, **kwargs):
        connect = redis.StrictRedis(host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=settings.REDIS_SPACE,
                                    password=settings.REDIS_PASSWD)
        status_json = connect.get('MANAGER_STATUS')
        if status_json is None:
            manager_status = {}
        else:
            manager_status = json.loads(str(status_json, encoding='utf-8'))
        return Response(manager_status,status.HTTP_200_OK)
