# -*- coding:utf-8 -*-
# !/usr/bin/env python
# Time 18-3-19
# Author Yo
# Email YoLoveLife@outlook.com
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated,AllowAny
from rest_framework.pagination import PageNumberPagination
from rest_framework.views import Response, status
from deveops.api import WebTokenAuthentication
# from zdb.permission import instance_group as InstanceGroupPermission
from zdb import models,serializers,filter

__all__ = [
    "ZDBInstanceGroupListAPI", "ZDBInstanceGroupCreateAPI", "ZDBInstanceGroupDeleteAPI",
    "ZDBInstanceGroupListByPageAPI", "ZDBInstanceGroupUpdateAPI", "ZDBInstancePagination"
]

class ZDBInstancePagination(PageNumberPagination):
    page_size = 10


class ZDBInstanceGroupListAPI(WebTokenAuthentication, generics.ListAPIView):
    module = models.InstanceGroup
    serializer_class = serializers.ZDBInstanceGroupSerializer
    queryset = models.InstanceGroup.objects.all()
    # permission_classes = [InstancePermission.DBInstanceListRequiredMixin, IsAuthenticated]
    permission_classes = [AllowAny,]
    filter_class = filter.ZDBInstanceGroupFilter


class ZDBInstanceGroupListByPageAPI(WebTokenAuthentication, generics.ListAPIView):
    module = models.InstanceGroup
    serializer_class = serializers.ZDBInstanceGroupSerializer
    queryset = models.InstanceGroup.objects.all()
    # permission_classes = [InstancePermission.DBInstanceListRequiredMixin, IsAuthenticated]
    permission_classes = [AllowAny,]
    pagination_class = ZDBInstancePagination
    filter_class = filter.ZDBInstanceGroupFilter


class ZDBInstanceGroupCreateAPI(WebTokenAuthentication, generics.CreateAPIView):
    module = models.InstanceGroup
    serializer_class = serializers.ZDBInstanceGroupSerializer
    queryset = models.InstanceGroup.objects.all()
    # permission_classes = [InstancePermission.DBInstanceCreateRequiredMixin, IsAuthenticated]
    permission_classes = [AllowAny,]


class ZDBInstanceGroupUpdateAPI(WebTokenAuthentication, generics.UpdateAPIView):
    module = models.InstanceGroup
    serializer_class = serializers.ZDBInstanceGroupSerializer
    queryset = models.InstanceGroup.objects.all()
    # permission_classes = [InstancePermission.DBInstanceUpdateRequiredMixin, IsAuthenticated]
    permission_classes = [AllowAny,]
    lookup_url_kwarg = 'pk'
    lookup_field = 'uuid'


class ZDBInstanceGroupDeleteAPI(WebTokenAuthentication, generics.DestroyAPIView):
    module = models.InstanceGroup
    serializer_class = serializers.ZDBInstanceGroupSerializer
    queryset = models.InstanceGroup.objects.all()
    # permission_classes = [InstancePermission.DBInstanceDeleteRequiredMixin, IsAuthenticated]
    permission_classes = [AllowAny,]
    lookup_url_kwarg = 'pk'
    lookup_field = 'uuid'

    def delete(self, request, *args, **kwargs):
        instance_group = self.get_object()
        if instance_group.instances.exists():
            return Response({'detail':'该实例组下还存在实例'}, status=status.HTTP_406_NOT_ACCEPTABLE)
        else:
            return super(ZDBInstanceGroupDeleteAPI,self).delete(request, *args, **kwargs)

