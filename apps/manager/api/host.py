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
from manager.permission import host as HostPermission
from deveops.api import WebTokenAuthentication

__all__ = [
    'ManagerHostListAPI', 'ManagerHostCreateAPI',
    'ManagerHostUpdateAPI','ManagerHostDeleteAPI',
    'HostPagination', 'ManagerHostListByPageAPI'
]


class HostPagination(PageNumberPagination):
    page_size = 10


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


class ManagerHostUpdateAPI(WebTokenAuthentication, generics.UpdateAPIView):
    module = models.Host
    serializer_class = serializers.HostSerializer
    queryset = models.Host.objects.all()
    permission_classes = [HostPermission.HostUpdateRequiredMixin, IsAuthenticated]
    lookup_field = "uuid"
    lookup_url_kwarg = "pk"


class ManagerHostDeleteAPI(WebTokenAuthentication, generics.DestroyAPIView):
    module = models.Host
    serializer_class = serializers.HostSerializer
    queryset = models.Host.objects.all()
    permission_classes = [HostPermission.HostDeleteRequiredMixin, IsAuthenticated]
    lookup_field = 'uuid'
    lookup_url_kwarg = 'pk'
    # def delete(self, request, *args, **kwargs):
    #     host = models.Host.objects.get(id=int(kwargs['pk']))
    #     if host.storages.count() != 0:
    #         return Response({'detail': '该主机下存在存储无法删除'}, status=status.HTTP_406_NOT_ACCEPTABLE)
    #     elif len(host.application_get()) !=0:
    #         return Response({'detail': '该主机下存在应用无法删除'}, status=status.HTTP_406_NOT_ACCEPTABLE)
    #     else:
    #         apps.manager.models.Host.objects.get(id=int(kwargs['pk'])).delete()
    #         return Response({'detail': '删除成功'}, status=status.HTTP_201_CREATED)


class ManagerHostPasswordAPI(WebTokenAuthentication, generics.ListAPIView):
    serializer_class = serializers.HostPasswordSerializer
    permission_classes = [HostPermission.HostPasswordRequiredMixin, IsAuthenticated]
    lookup_field = 'uuid'
    lookup_url_kwarg = 'pk'

    def get_queryset(self):# 此处时由于RestFramework的permission会被调用两次 只能在这里使用装饰器
        host = models.Host.objects.filter(uuid=self.kwargs['pk'])
        return host

    def get(self, request, *args, **kwargs):
        if self.request.user.check_qrcode(kwargs['qrcode']):
            return super(ManagerHostPasswordAPI,self).get(request, *args, **kwargs)
        else:
            return Response({'detail': '您的QR-Code有误'}, status=status.HTTP_406_NOT_ACCEPTABLE)


class ManagerHostSelectGroupAPI(WebTokenAuthentication, generics.UpdateAPIView):
    serializer_class = serializers.HostSelectGroupSerializer
    permission_classes = [HostPermission.HostSelectGroupRequiredMixin , IsAuthenticated]
    queryset = models.Host.objects.all()
    lookup_field = 'uuid'
    lookup_url_kwarg = 'pk'

