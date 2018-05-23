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
from deveops.conf import REDIS_PORT,REDIS_SPACE

__all__ = [
    "DashboardManagerAPI",
]


class DashboardManagerAPI(WebTokenAuthentication,generics.ListAPIView):
    permission_classes = [AllowAny,]
    # def get(self, request, *args, **kwargs):

    def get(self, request, *args, **kwargs):
        con = redis.StrictRedis(port=REDIS_PORT,db=REDIS_SPACE)
        status_json = con.get('MANAGER_STATUS')
        manager_status = json.loads(str(status_json, encoding='utf-8'))
        return Response(manager_status,status.HTTP_200_OK)
