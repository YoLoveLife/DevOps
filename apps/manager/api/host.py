# -*- coding:utf-8 -*-
# !/usr/bin/env python
# Time 18-3-19
# Author Yo
# Email YoLoveLife@outlook.com
from .. import models, serializers
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated,AllowAny
from rest_framework.pagination import PageNumberPagination
from rest_framework.views import Response, status
from manager.permission import host as HostPermission
from deveops.api import WebTokenAuthentication

__all__ = [
    'ManagerHostListAPI', 'ManagerHostCreateAPI',
    'ManagerHostDetailAPI','ManagerHostUpdateAPI','ManagerHostDeleteAPI',
    'HostPagination', 'ManagerHostListByPageAPI'
]


class HostPagination(PageNumberPagination):
    page_size = 10


class ManagerHostListAPI(WebTokenAuthentication,generics.ListAPIView):
    module = models.Host
    serializer_class = serializers.HostSerializer
    queryset = models.Host.objects.all()
    permission_classes = [HostPermission.HostListRequiredMixin,IsAuthenticated]


class ManagerHostListByPageAPI(WebTokenAuthentication, generics.ListAPIView):
    module = models.Host
    serializer_class = serializers.HostSerializer
    queryset = models.Host.objects.all()
    permission_classes = [HostPermission.HostListRequiredMixin,IsAuthenticated]
    pagination_class = HostPagination


class ManagerHostCreateAPI(WebTokenAuthentication,generics.CreateAPIView):
    module = models.Host
    serializer_class = serializers.HostSerializer
    permission_classes = [HostPermission.HostCreateRequiredMixin,IsAuthenticated]


class ManagerHostDetailAPI(WebTokenAuthentication,APIView):
    # permission_classes = [HostPermission.HostDetailRequiredMixin,IsAuthenticated]
    permission_classes = [AllowAny]

    def get_object(self):
        return models.Host.objects.filter(id=int(self.kwargs['pk'])).get()

    def get(self, request, *args, **kwargs):
        from deveops.utils import aliyun
        from deveops.utils import vmware
        obj = self.get_object()
        data = None
        if obj.detail.aliyun_id:
            data = aliyun.fetch_Instance(obj.detail.aliyun_id)
            if data:
                data['type'] = 'aliyun'
            else:
                return Response(data, status=status.HTTP_406_NOT_ACCEPTABLE)
            return Response(data, status=status.HTTP_200_OK)
        elif obj.detail.vmware_id:
            data = vmware.fetch_Instance(obj.detail.vmware_id)
            if data:
                data['type'] = 'vmware'
            else:
                return Response(data, status=status.HTTP_406_NOT_ACCEPTABLE)
            return Response(data, status=status.HTTP_200_OK)
        else:
            return Response(data, status=status.HTTP_406_NOT_ACCEPTABLE)


class ManagerHostUpdateAPI(WebTokenAuthentication,generics.UpdateAPIView):
    module = models.Host
    serializer_class = serializers.HostSerializer
    queryset = models.Host.objects.all()
    # permission_classes = [HostPermission.HostUpdateRequiredMixin,IsAuthenticated]
    permission_classes = [AllowAny]


class ManagerHostDeleteAPI(WebTokenAuthentication,generics.DestroyAPIView):
    module = models.Host
    serializer_class = serializers.HostSerializer
    queryset = models.Host.objects.all()
    permission_classes = [HostPermission.HostDeleteRequiredMixin,IsAuthenticated]

    # def delete(self, request, *args, **kwargs):
    #     host = models.Host.objects.get(id=int(kwargs['pk']))
    #     if host.storages.count() != 0:
    #         return Response({'detail': '该主机下存在存储无法删除'}, status=status.HTTP_406_NOT_ACCEPTABLE)
    #     elif len(host.application_get()) !=0:
    #         return Response({'detail': '该主机下存在应用无法删除'}, status=status.HTTP_406_NOT_ACCEPTABLE)
    #     else:
    #         apps.manager.models.Host.objects.get(id=int(kwargs['pk'])).delete()
    #         return Response({'detail': '删除成功'}, status=status.HTTP_201_CREATED)


class ManagerHostPasswordAPI(WebTokenAuthentication,generics.ListAPIView):
    serializer_class = serializers.HostPasswordSerializer
    # permission_classes = [HostPermission.HostPasswordRequiredMixin,IsAuthenticated]
    permission_classes = [AllowAny]
    #
    # @decorator_manager(5, u'获取密码')
    # def timeline_create(self,user):
    #     return user,None

    def get_queryset(self):#此处时由于RestFramework的permission会被调用两次 只能在这里使用装饰器
        # if self.count == 0:
        #     self.count = self.count + 1
        #     self.timeline_create(self.request.user)
        host = models.Host.objects.filter(id=int(self.kwargs['pk']))
        return host