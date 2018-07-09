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
from dashboard.permission import expired as ExpirePermission

__all__ = [
    "ExpiredPagination",
    "DashboardExpiredECSAPI",
    "DashboardExpiredRDSAPI",
]


class ExpiredPagination(PageNumberPagination):
    page_size = 10


class DashboardExpiredECSAPI(WebTokenAuthentication,generics.ListAPIView):
    module = models.ExpiredAliyunECS
    permission_classes = [ExpirePermission.ExpiredListRequiredMixin, IsAuthenticated]
    queryset = models.ExpiredAliyunECS.objects.all()
    serializer_class = serializers.DashboardExpiredAliyunECSSerializer
    pagination_class = ExpiredPagination


class DashboardExpiredRDSAPI(WebTokenAuthentication,generics.ListAPIView):
    module = models.ExpiredAliyunRDS
    permission_classes = [ExpirePermission.ExpiredListRequiredMixin, IsAuthenticated]
    queryset = models.ExpiredAliyunRDS.objects.all()
    serializer_class = serializers.DashboardExpiredAliyunRDSSerializer
    pagination_class = ExpiredPagination

class DashboardExpiredKVStoreAPI(WebTokenAuthentication, generics.ListAPIView):
    module = models.ExpiredAliyunKVStore
    permission_classes = [ExpirePermission.ExpiredListRequiredMixin, IsAuthenticated]
    queryset = models.ExpiredAliyunKVStore.objects.all()
    serializer_class = serializers.DashboardExpiredAliyunKVStoreSerializer
    pagination_class = ExpiredPagination


class DashboardExpiredMongoDBAPI(WebTokenAuthentication, generics.ListAPIView):
    module = models.ExpiredAliyunMongoDB
    permission_classes = [ExpirePermission.ExpiredListRequiredMixin, IsAuthenticated]
    queryset = models.ExpiredAliyunMongoDB.objects.all()
    serializer_class = serializers.DashboardExpiredAliyunMongoDBSerializer
    pagination_class = ExpiredPagination