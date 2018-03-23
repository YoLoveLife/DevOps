# -*- coding:utf-8 -*-
# !/usr/bin/env python
# Time 18-3-19
# Author Yo
# Email YoLoveLife@outlook.com
from .. import models,serializers
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import Response,status
from rest_framework.pagination import PageNumberPagination
from manager.permission import group as GroupPermission
from manager.permission import host as HostPermission
from manager.permission import storage as StoragePermission
from timeline.decorator.manager import decorator_manager
from deveops.api import WebTokenAuthentication

class ManagerHostListByGroupAPI(WebTokenAuthentication,generics.ListAPIView):
    module = models.Host
    serializer_class = serializers.HostSerializer
    # permission_classes = [IsAuthenticated]
    # pagination_class = PagePa

    def get_queryset(self):
        if self.kwargs['pk']=='0':
            queryset = models.Host.objects.all()
            return queryset
        queryset= models.Group.objects.get(id=self.kwargs['pk']).hosts
        return queryset
    #
    # def paginate_queryset(self, queryset):

class ManagerHostListAPI(WebTokenAuthentication,generics.ListAPIView):
    module = models.Host
    serializer_class = serializers.HostSerializer
    queryset = models.Host.objects.all()
    permission_classes = [IsAuthenticated]


class ManagerHostCreateAPI(WebTokenAuthentication,generics.CreateAPIView):
    module = models.Host
    serializer_class = serializers.HostSerializer
    permission_classes = [IsAuthenticated]


class ManagerHostDetailAPI(WebTokenAuthentication,generics.ListAPIView):
    module = models.Host
    serializer_class = serializers.HostSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = models.Host.objects.filter(id=self.kwargs['pk'])
        return queryset

class ManagerHostUpdateAPI(WebTokenAuthentication,generics.UpdateAPIView):
    module = models.Host
    serializer_class = serializers.HostSerializer
    permission_classes = [IsAuthenticated]
    queryset = models.Host.objects.all()

class ManagerHostDeleteAPI(WebTokenAuthentication,generics.DestroyAPIView):
    module = models.Host
    serializer_class = serializers.HostSerializer
    # permission_classes = [HostPermission.HostDeleteRequiredMixin]
    queryset = models.Host.objects.all()

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
    # permission_classes = (HostPermission.HostPasswordRequiredMixin,)
    # count = 0
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