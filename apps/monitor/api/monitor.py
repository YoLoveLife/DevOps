# -*- coding:utf-8 -*-
# !/usr/bin/env python
# Time 18-3-19
# Author Yo
# Email YoLoveLife@outlook.com
from .. import models
from manager.models import Host
import json
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated,AllowAny
from rest_framework.pagination import PageNumberPagination
from rest_framework.views import Response, status
from deveops.api import WebTokenAuthentication
from monitor.permission import monitor as MonitorPermission
__all__ = [
    'MonitorPagination', 'MonitorHostAliyunDetailCPUAPI'
]


class MonitorPagination(PageNumberPagination):
    page_size = 10


class MonitorHostAliyunDetailCPUAPI(WebTokenAuthentication, APIView):
    # permission_classes = [MonitorPermission.MonitorAliyunAPIRequiredMixin, IsAuthenticated]
    permission_classes = [AllowAny,]

    def get_object(self):
        return Host.objects.filter(uuid=self.kwargs['pk']).get()

    def get(self, request, *args, **kwargs):
        from deveops.tools.aliyun.cms import AliyunECSCMSTool
        API = AliyunECSCMSTool()
        API.request_to_period(API, '900')
        API.request_to_day(API)
        API.request_to_instance(API,self.get_object().detail.aliyun_id)
        API.get_cpu_results()
        results = API.get_line_opts(API.get_results(), 'CPU使用率')
        return Response(results, status.HTTP_200_OK)


class MonitorHostAliyunDetailMemoryAPI(WebTokenAuthentication, APIView):
    permission_classes = [AllowAny,]

    def get_object(self):
        return Host.objects.filter(uuid=self.kwargs['pk']).get()

    def get(self, request, *args, **kwargs):
        from deveops.tools.aliyun.cms import AliyunECSCMSTool
        API = AliyunECSCMSTool()
        API.request_to_period(API, '900')
        API.request_to_day(API)
        API.request_to_instance(API,self.get_object().detail.aliyun_id)
        API.get_mem_results()
        results = API.get_line_opts(API.get_results(), '内存使用率')
        return Response(results, status.HTTP_200_OK)