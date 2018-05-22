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
from deveops.conf import REDIS_PORT,REDIS_SPACE
__all__ = [

]


class ManagerDashboardAPI(WebTokenAuthentication,generics.ListAPIView):
    permission_classes = [AllowAny,]
    # def get(self, request, *args, **kwargs):

    def get(self, request, *args, **kwargs):
        con = redis.StrictRedis(port=REDIS_PORT,db=REDIS_SPACE)
        print(con.hgetall('MANAGER_STATUS'))
        return Response(con.hgetall('MANAGER_STATUS'),status.HTTP_200_OK)
