# -*- coding:utf-8 -*-
# !/usr/bin/env python
# Time 18-3-19
# Author Yo
# Email YoLoveLife@outlook.com
from .. import models, serializers
from django.conf import settings
from django.db.models import Q
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated,AllowAny
from rest_framework.pagination import PageNumberPagination
from rest_framework.views import Response, status
from utils.permission import file as FilePermission
import datetime
from deveops.api import WebTokenAuthentication

__all__ = [
    'FilePagination', 'UtilsFileCreateAPI',
    'UtilsFileListAPI', 'UtilsFileListByPageAPI',
    'UtilsFileDeleteAPI',
]


class FilePagination(PageNumberPagination):
    page_size = 10


class UtilsFileListAPI(WebTokenAuthentication,generics.ListAPIView):
    module = models.FILE
    serializer_class = serializers.FileSerializer
    permission_classes = [FilePermission.FileListRequiredMixin, IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        end_time = datetime.datetime.now().strftime('%Y-%m-%d')
        start_time = (datetime.datetime.now() - datetime.timedelta(days=2)).strftime('%Y-%m-%d')
        query_set = models.FILE.objects.filter(user=user,
                                               pushmission__isnull=False,
                                               create_time__range=(start_time, end_time))
        return query_set


class UtilsFileListByPageAPI(WebTokenAuthentication, generics.ListAPIView):
    module = models.FILE
    serializer_class = serializers.FileSerializer
    permission_classes = [FilePermission.FileListRequiredMixin, IsAuthenticated]
    pagination_class = FilePagination

    def get_queryset(self):
        user = self.request.user
        query_set = models.FILE.objects.filter(user=user,)
        return query_set



class UtilsFileCreateAPI(WebTokenAuthentication, generics.CreateAPIView):
    module = models.FILE
    serializer_class = serializers.FileSerializer
    permission_classes = [FilePermission.FileCreateRequiredMixin, IsAuthenticated]


class UtilsFileUpdateAPI(WebTokenAuthentication, generics.UpdateAPIView):
    module = models.FILE
    serializer_class = serializers.FileSerializer
    permission_classes = [FilePermission.FileUpdateRequiredMixin, IsAuthenticated]
    lookup_field = 'uuid'
    lookup_url_kwarg = 'pk'

    def get_queryset(self):
        user = self.request.user
        query_set = models.FILE.objects.filter(user=user,)
        return query_set



class UtilsFileDeleteAPI(WebTokenAuthentication, generics.DestroyAPIView):
    module = models.FILE
    serializer_class = serializers.FileSerializer
    queryset = models.FILE.objects.all()
    permission_classes = [FilePermission.FileDeleteRequiredMixin, IsAuthenticated]
    lookup_field = 'uuid'
    lookup_url_kwarg = 'pk'

    def delete(self, request, *args, **kwargs):
        obj = self.get_object()
        if not obj.pushmission.exists():
            return super(UtilsFileDeleteAPI, self).delete(request, *args, **kwargs)
        else:
            return Response({'detail': '该文件已经属于某个任务无法被删除'}, status=status.HTTP_406_NOT_ACCEPTABLE)

