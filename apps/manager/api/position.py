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


class ManagerPositionListAPI(generics.ListAPIView):
    module = models.Position
    serializer_class = serializers.PositionSerializer
    permission_classes = [IsAuthenticated]
    queryset = models.Position.objects.all()

class ManagerPositionCreateAPI(generics.CreateAPIView):
    module = models.Position
    serializer_class = serializers.PositionSerializer
    permission_classes = [IsAuthenticated]

class ManagerPositionDetailAPI(generics.ListAPIView):
    module = models.Position
    serializer_class = serializers.PositionSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return models.Position.objects.filter(id=int(self.kwargs['pk']))

class ManagerPositionUpdateAPI(generics.UpdateAPIView):
    module = models.Position
    serializer_class = serializers.PositionSerializer
    permission_classes = [IsAuthenticated]
    queryset = models.Position.objects.all()

class ManagerPositionDeleteAPI(generics.DestroyAPIView):
    module = models.Position
    serializer_class = serializers.PositionSerializer
    # permission_classes = [GroupPermission.GroupDeleteRequiredMixin]
    queryset = models.Position.objects.all()