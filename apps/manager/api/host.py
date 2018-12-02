# -*- coding:utf-8 -*-
# !/usr/bin/env python
# Time 18-3-19
# Author Yo
# Email YoLoveLife@outlook.com
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.pagination import PageNumberPagination
from rest_framework.views import Response, status
from manager.permission import host as HostPermission
from .. import models, serializers, filter
from deveops.api import WebTokenAuthentication
from timeline.decorator import decorator_api
from django.conf import settings

__all__ = [
    'ManagerHostListAPI', 'ManagerHostCreateAPI',
    'ManagerHostUpdateAPI', 'ManagerHostDeleteAPI',
    'HostPagination', 'ManagerHostListByPageAPI'
]


class HostPagination(PageNumberPagination):
    page_size = 10
    max_page_size = 60
    page_size_query_param = 'page_size'


class ManagerHostListAPI(WebTokenAuthentication, generics.ListAPIView):
    module = models.Host
    queryset = models.Host.objects.all()
    serializer_class = serializers.HostSampleSerializer
    permission_classes = [HostPermission.HostListRequiredMixin, IsAuthenticated]
    filter_class = filter.HostFilter


class ManagerHostListByPageAPI(ManagerHostListAPI):
    module = models.Host
    serializer_class = serializers.HostSerializer
    queryset = models.Host.objects.all()
    permission_classes = [HostPermission.HostListRequiredMixin, IsAuthenticated]
    pagination_class = HostPagination
    filter_class = filter.HostFilter


class ManagerHostCreateAPI(WebTokenAuthentication, generics.CreateAPIView):
    module = models.Host
    serializer_class = serializers.HostSerializer
    permission_classes = [HostPermission.HostCreateRequiredMixin, IsAuthenticated]
    msg = settings.LANGUAGE.ManagerHostCreateAPI

    @decorator_api(timeline_type=settings.TIMELINE_KEY_VALUE['Host_HOST_CREATE'])
    def create(self, request, *args, **kwargs):
        if self.qrcode_check(request):
            response = super(ManagerHostCreateAPI, self).create(request, *args, **kwargs)
            return self.msg.format(
                USER=request.user.full_name,
                HOSTNAME=response.data['hostname'],
                CONNECT_IP=response.data['connect_ip'],
                UUID=response.data['uuid'],
            ), response
        else:
            return '', self.qrcode_response


class ManagerHostUpdateAPI(WebTokenAuthentication, generics.UpdateAPIView):
    module = models.Host
    serializer_class = serializers.HostSerializer
    queryset = models.Host.objects.all()
    permission_classes = [HostPermission.HostUpdateRequiredMixin, IsAuthenticated]
    lookup_field = "uuid"
    lookup_url_kwarg = "pk"
    msg = settings.LANGUAGE.ManagerHostUpdateAPI

    @decorator_api(timeline_type=settings.TIMELINE_KEY_VALUE['Host_HOST_UPDATE'])
    def update(self, request, *args, **kwargs):
        if self.qrcode_check(request):
            response = super(ManagerHostUpdateAPI, self).update(request, *args, **kwargs)
            host = self.get_object()
            return self.msg.format(
                USER=request.user.full_name,
                HOSTNAME=host.hostname,
                CONNECT_IP=host.connect_ip,
                UUID=host.uuid,
            ), response
        else:
            return '', self.qrcode_response


class ManagerHostDeleteAPI(WebTokenAuthentication, generics.DestroyAPIView):
    module = models.Host
    serializer_class = serializers.HostSerializer
    queryset = models.Host.objects.all()
    permission_classes = [HostPermission.HostDeleteRequiredMixin, IsAuthenticated]
    lookup_field = 'uuid'
    lookup_url_kwarg = 'pk'
    msg = settings.LANGUAGE.ManagerHostDeleteAPI

    @decorator_api(timeline_type=settings.TIMELINE_KEY_VALUE['Host_HOST_DELETE'])
    def delete(self, request, *args, **kwargs):
        if self.qrcode_check(request):
            host = self.get_object()
            response = super(ManagerHostDeleteAPI, self).delete(request, *args, **kwargs)
            return self.msg.format(
                USER=request.user.full_name,
                HOSTNAME=host.hostname,
                CONNECT_IP=host.connect_ip,
                UUID=host.uuid,
            ), response
        else:
            return '', self.qrcode_response


class ManagerHostPasswordAPI(WebTokenAuthentication, generics.ListAPIView):
    serializer_class = serializers.HostPasswordSerializer
    permission_classes = [HostPermission.HostPasswordRequiredMixin, IsAuthenticated]
    lookup_field = 'uuid'
    lookup_url_kwarg = 'pk'

    def get_queryset(self):
        host = models.Host.objects.filter(uuid=self.kwargs['pk'])
        return host

    def get(self, request, *args, **kwargs):
        if self.request.user.check_qrcode(kwargs['qrcode']):
            return super(ManagerHostPasswordAPI, self).get(request, *args, **kwargs)
        else:
            return self.qrcode_response


class ManagerHostSelectGroupAPI(WebTokenAuthentication, generics.UpdateAPIView):
    serializer_class = serializers.HostSelectGroupSerializer
    permission_classes = [HostPermission.HostSelectGroupRequiredMixin, IsAuthenticated]
    queryset = models.Host.objects.all()
    lookup_field = 'uuid'
    lookup_url_kwarg = 'pk'
    msg = settings.LANGUAGE.ManagerHostSelectGroupAPI

    @decorator_api(timeline_type=settings.TIMELINE_KEY_VALUE['Host_HOST_SORT'])
    def update(self, request, *args, **kwargs):
        if self.qrcode_check(request):
            host = self.get_object()
            response = super(ManagerHostSelectGroupAPI, self).update(request, *args, **kwargs)
            return self.msg.format(
                USER=request.user.full_name,
                HOSTNAME=host.hostname,
                CONNECT_IP=host.connect_ip,
                UUID=host.uuid,
            ), response
        else:
            return '', self.qrcode_response

