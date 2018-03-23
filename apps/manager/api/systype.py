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

class ManagerSystypeListAPI(WebTokenAuthentication,generics.ListAPIView):
    module = models.System_Type
    serializer_class = serializers.SystemTypeSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = models.System_Type.objects.all()
        return queryset

class ManagerSystemCreateAPI(WebTokenAuthentication,generics.CreateAPIView):
    module = models.System_Type
    serializer_class = serializers.SystemTypeSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        if models.System_Type.objects.filter(name=request.data['name']).count()>0:
            return Response({'detail': '所添加的SystemType已存在'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
        else:
            return super(ManagerSystemCreateAPI,self).create(request,*args,**kwargs)

class ManagerSystemDetailAPI(WebTokenAuthentication,generics.ListAPIView):
    module = models.System_Type
    serializer_class = serializers.SystemTypeSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return models.System_Type.objects.filter(id=int(self.kwargs['pk']))

class ManagerSystemUpdateAPI(WebTokenAuthentication,generics.UpdateAPIView):
    module = models.System_Type
    serializer_class = serializers.SystemTypeSerializer
    # permission_classes = [IsAuthenticated]
    queryset = models.System_Type.objects.all()

class ManagerSystemDeleteAPI(WebTokenAuthentication,generics.DestroyAPIView):
    module = models.System_Type
    serializer_class = serializers.SystemTypeSerializer
    # permission_classes = [GroupPermission.GroupDeleteRequiredMixin]
    queryset = models.System_Type.objects.all()
