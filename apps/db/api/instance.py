# -*- coding:utf-8 -*-
# !/usr/bin/env python
# Time 18-3-19
# Author Yo
# Email YoLoveLife@outlook.com
from db import models,serializers,filter
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated,AllowAny
from deveops.api import WebTokenAuthentication
from rest_framework.pagination import PageNumberPagination
from rest_framework.views import Response, status

__all__ = [
    "DBInstancePagination", "DBInstanceListAPI",
    "DBInstanceListByPageAPI"
]


class DBInstancePagination(PageNumberPagination):
    page_size = 10


class DBInstanceListAPI(WebTokenAuthentication, generics.ListAPIView):
    module = models.Instance
    serializer_class = serializers.DBInstanceSerializer
    queryset = models.Instance.objects.all()
    permission_classes = [AllowAny,]
    filter_class = filter.DBInstanceFilter


class DBInstanceListByPageAPI(WebTokenAuthentication, generics.ListAPIView):
    module = models.Instance
    serializer_class = serializers.DBInstanceSerializer
    queryset = models.Instance.objects.all()
    permission_classes = [AllowAny,]
    pagination_class = DBInstancePagination
    filter_class = filter.DBInstanceFilter


class DBInstanceCreateAPI(WebTokenAuthentication, generics.CreateAPIView):
    module = models.Instance
    serializer_class = serializers.DBInstanceSerializer
    queryset = models.Instance.objects.all()
    permission_classes = [AllowAny,]

    def create(self, request, *args, **kwargs):
        return super(DBInstanceCreateAPI, self).create(request, *args, **kwargs)


class DBInstanceUpdateAPI(WebTokenAuthentication, generics.UpdateAPIView):
    module = models.Instance
    serializer_class = serializers.DBInstanceSerializer
    queryset = models.Instance.objects.all()
    permission_classes = [AllowAny,]
    lookup_url_kwarg = 'pk'
    lookup_field = 'uuid'


# class DBInstanceDetailUpdateAPI(WebTokenAuthentication, generics.UpdateAPIView):
#     module = models.Instance
#     serializer_class =serializers.DBInstanceDetailSerializer
#     queryset = models.Instance.objects.all()
#     permission_classes = [AllowAny,]
#     lookup_url_kwarg = 'pk'
#     lookup_field = 'uuid'


class DBInstanceDeleteAPI(WebTokenAuthentication, generics.DestroyAPIView):
    module = models.Instance
    serializer_class = serializers.DBInstanceSerializer
    queryset = models.Instance.objects.all()
    permission_classes = [AllowAny,]
    lookup_url_kwarg = 'pk'
    lookup_field = 'uuid'

    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.roles.exists():
            return Response({'detail':'该实例下还存在角色'}, status=status.HTTP_406_NOT_ACCEPTABLE)
        else:
            return super(DBInstanceDeleteAPI,self).delete(request, *args, **kwargs)