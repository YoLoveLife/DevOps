# -*- coding:utf-8 -*-
# !/usr/bin/env python
# Time 18-3-19
# Author Yo
# Email YoLoveLife@outlook.com
from .. import models, serializers
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import Response, status
from manager.permission import position as PositionPermission
from deveops.api import WebTokenAuthentication

__all__ = [
    "ManagerPositionListAPI", "ManagerPositionCreateAPI", "ManagerPositionDetailAPI",
    "ManagerPositionUpdateAPI", "ManagerPositionDeleteAPI"
]


class ManagerPositionListAPI(WebTokenAuthentication,generics.ListAPIView):
    module = models.Position
    serializer_class = serializers.PositionSerializer
    queryset = models.Position.objects.all()
    permission_classes = [PositionPermission.PositionListRequiredMixin,IsAuthenticated]


class ManagerPositionCreateAPI(WebTokenAuthentication,generics.CreateAPIView):
    module = models.Position
    serializer_class = serializers.PositionSerializer
    permission_classes = [PositionPermission.PositionCreateRequiredMixin,IsAuthenticated]

    def create(self, request, *args, **kwargs):
        if models.Position.objects.filter(name=request.data['name']).count()>0:
            return Response({'detail': '所添加的Position已存在'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
        else:
            return super(ManagerPositionCreateAPI,self).create(request,*args,**kwargs)


class ManagerPositionDetailAPI(WebTokenAuthentication,generics.ListAPIView):
    module = models.Position
    serializer_class = serializers.PositionSerializer
    permission_classes = [PositionPermission.PositionDetailRequiredMixin,IsAuthenticated]

    def get_queryset(self):
        return models.Position.objects.filter(id=int(self.kwargs['pk']))


class ManagerPositionUpdateAPI(WebTokenAuthentication,generics.UpdateAPIView):
    module = models.Position
    serializer_class = serializers.PositionSerializer
    queryset = models.Position.objects.all()
    permission_classes = [PositionPermission.PositionUpdateRequiredMixin,IsAuthenticated]
    lookup_field = 'uuid'
    lookup_url_kwarg = 'pk'

class ManagerPositionDeleteAPI(WebTokenAuthentication,generics.DestroyAPIView):
    module = models.Position
    serializer_class = serializers.PositionSerializer
    queryset = models.Position.objects.all()
    permission_classes = [PositionPermission.PositionDeleteRequiredMixin,IsAuthenticated]
    lookup_field = 'uuid'
    lookup_url_kwarg = 'pk'