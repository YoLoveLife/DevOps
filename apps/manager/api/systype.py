# -*- coding:utf-8 -*-
# !/usr/bin/env python
# Time 18-3-19
# Author Yo
# Email YoLoveLife@outlook.com
from .. import models, serializers
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import Response, status
from manager.permission import systype as SysTypePermission
from deveops.api import WebTokenAuthentication

__all__ = [
    "ManagerSysTypeListAPI", "ManagerSysTypeCreateAPI", "ManagerSysTypeDetailAPI",
    "ManagerSysTypeUpdateAPI", "ManagerSysTypeDeleteAPI"
]


class ManagerSysTypeListAPI(WebTokenAuthentication,generics.ListAPIView):
    module = models.System_Type
    serializer_class = serializers.SystemTypeSerializer
    permission_classes = [SysTypePermission.SysTypeListRequiredMixin,IsAuthenticated]

    def get_queryset(self):
        queryset = models.System_Type.objects.all()
        return queryset


class ManagerSysTypeCreateAPI(WebTokenAuthentication,generics.CreateAPIView):
    module = models.System_Type
    serializer_class = serializers.SystemTypeSerializer
    permission_classes = [SysTypePermission.SysTypeCreateRequiredMixin,IsAuthenticated]

    def create(self, request, *args, **kwargs):
        if models.System_Type.objects.filter(name=request.data['name']).count()>0:
            return Response({'detail': '所添加的SystemType已存在'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
        else:
            return super(ManagerSysTypeCreateAPI,self).create(request,*args,**kwargs)


class ManagerSysTypeDetailAPI(WebTokenAuthentication,generics.ListAPIView):
    module = models.System_Type
    serializer_class = serializers.SystemTypeSerializer
    permission_classes = [SysTypePermission.SysTypeDetailRequiredMixin,IsAuthenticated]

    def get_queryset(self):
        return models.System_Type.objects.filter(id=int(self.kwargs['pk']))


class ManagerSysTypeUpdateAPI(WebTokenAuthentication,generics.UpdateAPIView):
    module = models.System_Type
    serializer_class = serializers.SystemTypeSerializer
    queryset = models.System_Type.objects.all()
    permission_classes = [SysTypePermission.SysTypeUpdateRequiredMixin,IsAuthenticated]
    lookup_field = 'uuid'
    lookup_url_kwarg = 'pk'

class ManagerSysTypeDeleteAPI(WebTokenAuthentication,generics.DestroyAPIView):
    module = models.System_Type
    serializer_class = serializers.SystemTypeSerializer
    queryset = models.System_Type.objects.all()
    permission_classes = [SysTypePermission.SysTypeDeleteRequiredMixin,IsAuthenticated]
    lookup_field = 'uuid'
    lookup_url_kwarg = 'pk'