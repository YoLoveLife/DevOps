# -*- coding:utf-8 -*-
# !/usr/bin/env python
# Time 18-3-19
# Author Yo
# Email YoLoveLife@outlook.com
from .. import models, serializers
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated,AllowAny
from rest_framework.pagination import PageNumberPagination
from rest_framework.views import Response, status
from manager.permission import group as GroupPermission
from deveops.api import WebTokenAuthentication

__all__ = [
    'ManagerGroupListAPI', 'ManagerGroupCreateAPI', 'ManagerGroupDetailAPI',
    'ManagerGroupUpdateAPI', 'ManagerGroupDeleteAPI',
    'GroupPagination', 'ManagerGroupListByPageAPI'
]


class ManagerGroupListAPI(WebTokenAuthentication,generics.ListAPIView):
    module = models.Group
    serializer_class = serializers.GroupSerializer
    queryset = models.Group.objects.all()
    # permission_classes = [GroupPermission.GroupListRequiredMixin,IsAuthenticated]
    permission_classes = [AllowAny,]


class GroupPagination(PageNumberPagination):
    page_size = 10


class ManagerGroupListByPageAPI(WebTokenAuthentication, generics.ListAPIView):
    module = models.Group
    serializer_class = serializers.GroupSerializer
    queryset = models.Group.objects.all()
    permission_classes = [GroupPermission.GroupListRequiredMixin,IsAuthenticated]
    pagination_class = GroupPagination


class ManagerGroupCreateAPI(WebTokenAuthentication,generics.CreateAPIView):
    module = models.Group
    serializer_class = serializers.GroupSerializer
    # permission_classes = [GroupPermission.GroupCreateRequiredMixin,IsAuthenticated]
    permission_classes = [AllowAny]


class ManagerGroupDetailAPI(WebTokenAuthentication,generics.ListAPIView):
    module = models.Group
    serializer_class = serializers.GroupSerializer
    permission_classes = [GroupPermission.GroupDetailRequiredMixin,IsAuthenticated]

    def get_queryset(self):
        return models.Group.objects.filter(id=int(self.kwargs['pk']))


class ManagerGroupUpdateAPI(WebTokenAuthentication,generics.UpdateAPIView):
    module = models.Group
    serializer_class = serializers.GroupSerializer
    queryset = models.Group.objects.all()
    # permission_classes = [GroupPermission.GroupUpdateRequiredMixin,IsAuthenticated]
    permission_classes = [AllowAny,]
    lookup_field = 'uuid'
    lookup_url_kwarg = 'pk'


class ManagerGroupDeleteAPI(WebTokenAuthentication,generics.DestroyAPIView):
    module = models.Group
    serializer_class = serializers.GroupSerializer
    queryset = models.Group.objects.all()
    # permission_classes = [GroupPermission.GroupDeleteRequiredMixin,IsAuthenticated]
    permission_classes = [AllowAny,]
    lookup_field = 'uuid'
    lookup_url_kwarg = 'pk'

    def delete(self, request, *args, **kwargs):
        # group = models.Group.objects.get(id=int(kwargs['pk']))
        group = self.get_object()
        if group.hosts.count() != 0:
            return Response({'detail': '该应用组下存在主机无法删除'}, status=status.HTTP_406_NOT_ACCEPTABLE)
        else:
            return super(ManagerGroupDeleteAPI,self).delete(request,*args,**kwargs)


class ManagerGroupSelectHostAPI(WebTokenAuthentication, generics.UpdateAPIView):
    module = models.Group
    serializer_class = serializers.GroupSelectHostSerializer
    queryset = models.Group.objects.all()
    permission_classes = [AllowAny,]
    # permission_classes = [GroupPermission.GroupUpdateRequiredMixin,IsAuthenticated]
    lookup_field = 'uuid'
    lookup_url_kwarg = 'pk'

