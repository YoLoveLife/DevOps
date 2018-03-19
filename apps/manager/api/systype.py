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
from rest_framework.renderers import JSONRenderer
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

# authentication_classes = (JSONWebTokenAuthentication,)
# renderer_classes = (JSONRenderer,)

class ManagerSystypeListAPI(generics.ListAPIView):
    module = models.System_Type
    serializer_class = serializers.SystemTypeSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = models.System_Type.objects.all()
        return queryset

class ManagerSystemCreateAPI(generics.CreateAPIView):
    module = models.System_Type
    serializer_class = serializers.SystemTypeSerializer
    permission_classes = [IsAuthenticated]

class ManagerSystemDetailAPI(generics.ListAPIView):
    module = models.System_Type
    serializer_class = serializers.SystemTypeSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return models.System_Type.objects.filter(id=int(self.kwargs['pk']))

class ManagerSystemUpdateAPI(generics.UpdateAPIView):
    module = models.System_Type
    serializer_class = serializers.SystemTypeSerializer
    # permission_classes = [IsAuthenticated]
    queryset = models.System_Type.objects.all()

class ManagerSystemDeleteAPI(generics.DestroyAPIView):
    module = models.System_Type
    serializer_class = serializers.SystemTypeSerializer
    # permission_classes = [GroupPermission.GroupDeleteRequiredMixin]
    queryset = models.System_Type.objects.all()
