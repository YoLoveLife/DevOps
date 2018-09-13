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
from django.conf import settings
from deveops.api import WebTokenAuthentication
from monitor.permission import monitor as MonitorPermission
__all__ = [
    'MonitorPagination', 'MonitorHostAliyunDetailCPUAPI', 'MonitorHostAliyunDetailMemoryAPI',
]


class MonitorPagination(PageNumberPagination):
    page_size = 10


def time_pick(obj, time):
    if time == settings.TYPE_MONITOR_ONE_HOUR:
        obj.request_to_hour(obj,1)
    elif time == settings.TYPE_MONITOR_SIX_HOUR:
        obj.request_to_hour(obj, 6)
    elif time == settings.TYPE_MONITOR_HALF_DAY:
        obj.request_to_hour(obj, 12)
    elif time == settings.TYPE_MONITOR_DAY:
        obj.request_to_day(obj, 1)
    elif time == settings.TYPE_MONITOR_3_DAY:
        obj.request_to_day(obj, 3)
    elif time == settings.TYPE_MONITOR_7_DAY:
        obj.request_to_day(obj, 7)
    else:
        obj.request_to_hour(obj, 1)


class MonitorHostAliyunDetailCPUAPI(WebTokenAuthentication, APIView):
    permission_classes = [MonitorPermission.MonitorAliyunAPIRequiredMixin, IsAuthenticated]

    def get_object(self):
        return Host.objects.filter(uuid=self.kwargs['pk']).get()

    def get(self, request, *args, **kwargs):
        from deveops.tools.aliyun.cms import AliyunECSCMSTool
        time = kwargs['time']
        API = AliyunECSCMSTool()
        time_pick(API, time)
        API.request_to_instance(API,self.get_object().aliyun_id)
        API.request_get_cpu_results()
        return Response({'title':'CPU利用率', 'dataset': API.change_timestamp(API.get_results())})


class MonitorHostAliyunDetailMemoryAPI(WebTokenAuthentication, APIView):
    permission_classes = [MonitorPermission.MonitorAliyunAPIRequiredMixin, IsAuthenticated]

    def get_object(self):
        return Host.objects.filter(uuid=self.kwargs['pk']).get()

    def get(self, request, *args, **kwargs):
        from deveops.tools.aliyun.cms import AliyunECSCMSTool
        time = kwargs['time']
        API = AliyunECSCMSTool()
        time_pick(API, time)
        API.request_to_instance(API,self.get_object().aliyun_id)
        API.request_get_mem_results()
        return Response({'title':'内存使用率', 'dataset': API.change_timestamp(API.get_results())})


class MonitorHostAliyunDetailIReadIOPS(WebTokenAuthentication, APIView):
    permission_classes = [MonitorPermission.MonitorAliyunAPIRequiredMixin, IsAuthenticated]

    def get_object(self):
        return Host.objects.filter(uuid=self.kwargs['pk']).get()

    def get(self, request, *args, **kwargs):
        from deveops.tools.aliyun.cms import AliyunECSCMSTool
        time = kwargs['time']
        API = AliyunECSCMSTool()
        time_pick(API, time)
        API.request_to_instance(API, self.get_object().aliyun_id)
        API.request_get_read_iops_results()
        return Response({'title': '磁盘读取Count/Second', 'dataset': API.change_timestamp(API.get_results())})


class MonitorHostAliyunDetailInternetInRate(WebTokenAuthentication, APIView):
    permission_classes = [MonitorPermission.MonitorAliyunAPIRequiredMixin, IsAuthenticated]

    def get_object(self):
        return Host.objects.filter(uuid=self.kwargs['pk']).get()

    def get(self, request, *args, **kwargs):
        from deveops.tools.aliyun.cms import AliyunECSCMSTool
        time = kwargs['time']
        API = AliyunECSCMSTool()
        time_pick(API, time)
        API.request_to_instance(API, self.get_object().aliyun_id)
        API.request_get_in_net_results()
        return Response({'title': '网络流入流量bits/s', 'dataset': API.change_timestamp(API.get_results())})