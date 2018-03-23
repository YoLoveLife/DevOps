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



class ManagerPositionListAPI(WebTokenAuthentication,generics.ListAPIView):
    module = models.Position
    serializer_class = serializers.PositionSerializer
    permission_classes = [IsAuthenticated]
    queryset = models.Position.objects.all()

class ManagerPositionCreateAPI(WebTokenAuthentication,generics.CreateAPIView):
    module = models.Position
    serializer_class = serializers.PositionSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        if models.Position.objects.filter(name=request.data['name']).count()>0:
            return Response({'detail': '所添加的Position已存在'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
        else:
            return super(ManagerPositionCreateAPI,self).create(request,*args,**kwargs)


class ManagerPositionDetailAPI(WebTokenAuthentication,generics.ListAPIView):
    module = models.Position
    serializer_class = serializers.PositionSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return models.Position.objects.filter(id=int(self.kwargs['pk']))

class ManagerPositionUpdateAPI(WebTokenAuthentication,generics.UpdateAPIView):
    module = models.Position
    serializer_class = serializers.PositionSerializer
    permission_classes = [IsAuthenticated]
    queryset = models.Position.objects.all()

class ManagerPositionDeleteAPI(WebTokenAuthentication,generics.DestroyAPIView):
    module = models.Position
    serializer_class = serializers.PositionSerializer
    # permission_classes = [GroupPermission.GroupDeleteRequiredMixin]
    queryset = models.Position.objects.all()