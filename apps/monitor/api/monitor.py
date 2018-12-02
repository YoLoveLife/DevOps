# -*- coding:utf-8 -*-
# !/usr/bin/env python
# Time 18-3-19
# Author Yo
# Email YoLoveLife@outlook.com
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.pagination import PageNumberPagination
from rest_framework.views import Response, status
from django.conf import settings
from manager.models import Host
from deveops.api import WebTokenAuthentication
from monitor.permission import monitor as MonitorPermission

__all__ = [
    'MonitorPagination', 'MonitorHostAliyunDetailCPUAPI', 'MonitorHostAliyunDetailMemoryAPI',
]


class MonitorPagination(PageNumberPagination):
    page_size = 10


class MonitorHostAliyunDetailCPUAPI(WebTokenAuthentication, APIView):
    permission_classes = [MonitorPermission.MonitorAliyunAPIRequiredMixin, IsAuthenticated]

    def get_object(self):
        return Host.objects.filter(uuid=self.kwargs['pk']).get()

    def get(self, request, *args, **kwargs):
        from deveops.tools.aliyun_v2.request.cms.ecs import AliyunCMSECSTool
        API = AliyunCMSECSTool()
        return Response({
            'title': settings.LANGUAGE.MonitorHostAliyunDetailCPUAPI,
            'dataset': API.tool_get_metric_cpu(self.get_object().aliyun_id, int(kwargs['time'])).__next__()
        })


class MonitorHostAliyunDetailMemoryAPI(WebTokenAuthentication, APIView):
    permission_classes = [MonitorPermission.MonitorAliyunAPIRequiredMixin, IsAuthenticated]

    def get_object(self):
        return Host.objects.filter(uuid=self.kwargs['pk']).get()

    def get(self, request, *args, **kwargs):
        from deveops.tools.aliyun_v2.request.cms.ecs import AliyunCMSECSTool
        API = AliyunCMSECSTool()
        return Response({
            'title': settings.LANGUAGE.MonitorHostAliyunDetailMemoryAPI,
            'dataset': API.tool_get_metric_mem(self.get_object().aliyun_id, int(kwargs['time'])).__next__()
        })


class MonitorHostAliyunDetailIReadIOPS(WebTokenAuthentication, APIView):
    permission_classes = [MonitorPermission.MonitorAliyunAPIRequiredMixin, IsAuthenticated]

    def get_object(self):
        return Host.objects.filter(uuid=self.kwargs['pk']).get()

    def get(self, request, *args, **kwargs):
        from deveops.tools.aliyun_v2.request.cms.ecs import AliyunCMSECSTool
        API = AliyunCMSECSTool()
        return Response({
            'title': settings.LANGUAGE.MonitorHostAliyunDetailIReadIOPS,
            'dataset': API.tool_get_metric_read_iops(self.get_object().aliyun_id, int(kwargs['time'])).__next__()
        })


class MonitorHostAliyunDetailInternetInRate(WebTokenAuthentication, APIView):
    permission_classes = [MonitorPermission.MonitorAliyunAPIRequiredMixin, IsAuthenticated]

    def get_object(self):
        return Host.objects.filter(uuid=self.kwargs['pk']).get()

    def get(self, request, *args, **kwargs):
        from deveops.tools.aliyun_v2.request.cms.ecs import AliyunCMSECSTool
        API = AliyunCMSECSTool()
        return Response({
            'title': settings.LANGUAGE.MonitorHostAliyunDetailInternetInRate,
            'dataset': API.tool_get_metric_net_in(self.get_object().aliyun_id, int(kwargs['time'])).__next__()
        })


class MonitorHostAliyunDetailDiskUse(WebTokenAuthentication, APIView):
    permission_classes = [MonitorPermission.MonitorAliyunAPIRequiredMixin, IsAuthenticated]

    def get_object(self):
        return Host.objects.filter(uuid=self.kwargs['pk']).get()

    def get(self, request, *args, **kwargs):
        from deveops.tools.aliyun_v2.request.cms.ecs import AliyunCMSECSTool
        API = AliyunCMSECSTool()
        return Response({
            'title': settings.LANGUAGE.MonitorHostAliyunDetailDiskUse,
            'dataset': API.tool_get_metric_disk_use(
                self.get_object().aliyun_id,
                int(kwargs['time'])).__next__()
        })
