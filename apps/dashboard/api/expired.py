# -*- coding:utf-8 -*-
# !/usr/bin/env python
# Time 18-5-22
# Author Yo
# Email YoLoveLife@outlook.com

from .. import models, serializers
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated,AllowAny
from rest_framework.pagination import PageNumberPagination
from rest_framework.views import Response, status
from deveops.api import WebTokenAuthentication
import redis
from deveops.conf import REDIS_PORT,REDIS_SPACE

__all__ = [
    "ExpiredPagination",
    "DashboardExpiredECSAPI",
    "DashboardExpiredRDSAPI",
]


class ExpiredPagination(PageNumberPagination):
    page_size = 10


class DashboardExpiredECSAPI(WebTokenAuthentication,generics.ListAPIView):
    module = models.ExpiredAliyunECS
    permission_classes = [AllowAny,]
    queryset = models.ExpiredAliyunECS.objects.all()
    serializer_class = serializers.DashboardExpiredAliyunECSSerializer
    pagination_class = ExpiredPagination


class DashboardExpiredRDSAPI(WebTokenAuthentication,generics.ListAPIView):
    module = models.ExpiredAliyunRDS
    permission_classes = [AllowAny,]
    queryset = models.ExpiredAliyunRDS.objects.all()
    serializer_class = serializers.DashboardExpiredAliyunRDSSerializer
    pagination_class = ExpiredPagination