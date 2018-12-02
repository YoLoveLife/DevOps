# -*- coding:utf-8 -*-
# !/usr/bin/env python
# Time 18-3-19
# Author Yo
# Email YoLoveLife@outlook.com
from .. import models, serializers, filter
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated,AllowAny
from rest_framework.pagination import PageNumberPagination
from rest_framework.views import Response, status
from deveops.api import WebTokenAuthentication
__all__ = [
    'PoolPagination'
]


class PoolPagination(PageNumberPagination):
    page_size = 7


class PoolListAPI(WebTokenAuthentication, generics.ListAPIView):
    module = models.IP_Pool
    queryset = models.IP_Pool.objects.all()
    serializer_class = serializers.PoolSerializer
    permission_classes = [IsAuthenticated, ]
    filter_class = filter.IPFilter
    pagination_class = PoolPagination
