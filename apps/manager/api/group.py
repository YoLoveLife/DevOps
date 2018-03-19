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


class ManagerGroupListAPI(generics.ListAPIView):
    module = models.Group
    serializer_class = serializers.GroupSerializer
    permission_classes = [IsAuthenticated]
    queryset = models.Group.objects.all()

class ManagerGroupCreateAPI(generics.CreateAPIView):
    module = models.Group
    serializer_class = serializers.GroupSerializer
    permission_classes = [IsAuthenticated]

class ManagerGroupDetailAPI(generics.ListAPIView):
    module = models.Group
    serializer_class = serializers.GroupSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return models.Group.objects.filter(id=int(self.kwargs['pk']))

class ManagerGroupUpdateAPI(generics.UpdateAPIView):
    module = models.Group
    serializer_class = serializers.GroupSerializer
    # permission_classes = [IsAuthenticated]
    queryset = models.Group.objects.all()

class ManagerGroupDeleteAPI(generics.DestroyAPIView):
    module = models.Group
    serializer_class = serializers.GroupSerializer
    permission_classes = [GroupPermission.GroupDeleteRequiredMixin]
    queryset = models.Group.objects.all()

    def delete(self, request, *args, **kwargs):
        group = models.Group.objects.get(id=int(kwargs['pk']))
        if group.hosts.count() != 0:
            return Response({'detail': '该应用组下存在主机无法删除'}, status=status.HTTP_406_NOT_ACCEPTABLE)
        else:
            return super(ManagerGroupDeleteAPI,self).delete(request,*args,**kwargs)