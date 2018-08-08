# -*- coding:utf-8 -*-
# !/usr/bin/env python
# Time 18-3-19
# Author Yo
# Email YoLoveLife@outlook.com
from zdb import models,serializers,filter
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated,AllowAny
from deveops.api import WebTokenAuthentication
from rest_framework.pagination import PageNumberPagination
from rest_framework.views import Response, status
from zdb.permission import instance as InstancePermission

__all__ = [
    "DBInstancePagination", "DBInstanceListAPI",
    "DBInstanceListByPageAPI", "DBInstanceCreateAPI", "DBInstanceDeleteAPI",
    "DBInstanceUpdateAPI",
]


class DBInstancePagination(PageNumberPagination):
    page_size = 10


class DBInstanceListAPI(WebTokenAuthentication, generics.ListAPIView):
    module = models.Instance
    serializer_class = serializers.ZDBInstanceSerializer
    queryset = models.Instance.objects.all()
    # permission_classes = [InstancePermission.DBInstanceListRequiredMixin, IsAuthenticated]
    permission_classes = [AllowAny,]
    filter_class = filter.DBInstanceFilter


class DBInstanceListByPageAPI(WebTokenAuthentication, generics.ListAPIView):
    module = models.Instance
    serializer_class = serializers.ZDBInstanceSerializer
    queryset = models.Instance.objects.all()
    # permission_classes = [InstancePermission.DBInstanceListRequiredMixin, IsAuthenticated]
    permission_classes = [AllowAny, ]
    pagination_class = DBInstancePagination
    filter_class = filter.DBInstanceFilter


class DBInstanceCreateAPI(WebTokenAuthentication, generics.CreateAPIView):
    module = models.Instance
    serializer_class = serializers.DBInstanceCreateSerializer
    queryset = models.Instance.objects.all()
    # permission_classes = [InstancePermission.DBInstanceCreateRequiredMixin, IsAuthenticated]
    permission_classes = [AllowAny, ]

    def create(self, request, *args, **kwargs):
        data = request.data
        if models.Instance.objects.filter(port=data['detail']['port'],host_id=data['host']).exists():
            return Response({'detail': '该主机上已经存在该实例信息'}, status=status.HTTP_406_NOT_ACCEPTABLE)
        else:
            return super(DBInstanceCreateAPI,self).create(request, *args, **kwargs)


class DBInstanceImportAPI(WebTokenAuthentication, generics.CreateAPIView):
    module = models.Instance
    serializer_class = serializers.DBInstanceImportSerializer
    queryset = models.Instance.objects.all()
    permission_classes = [AllowAny,]



class DBInstanceUpdateAPI(WebTokenAuthentication, generics.UpdateAPIView):
    module = models.Instance
    serializer_class = serializers.ZDBInstanceSerializer
    queryset = models.Instance.objects.all()
    # permission_classes = [InstancePermission.DBInstanceUpdateRequiredMixin, IsAuthenticated]
    permission_classes = [AllowAny, ]
    lookup_url_kwarg = 'pk'
    lookup_field = 'uuid'


class DBInstanceDeleteAPI(WebTokenAuthentication, generics.DestroyAPIView):
    module = models.Instance
    serializer_class = serializers.ZDBInstanceSerializer
    queryset = models.Instance.objects.all()
    # permission_classes = [InstancePermission.DBInstanceDeleteRequiredMixin, IsAuthenticated]
    permission_classes = [AllowAny, ]
    lookup_url_kwarg = 'pk'
    lookup_field = 'uuid'

    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.roles.exists():
            return Response({'detail':'该实例下还存在角色'}, status=status.HTTP_406_NOT_ACCEPTABLE)
        else:
            return super(DBInstanceDeleteAPI,self).delete(request, *args, **kwargs)