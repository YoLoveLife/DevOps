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
from utils.permission import file as FilePermission
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
    queryset = models.FILE.objects.all()
    serializer_class = serializers.FileSerializer
    permission_classes = [AllowAny, ]
    # permission_classes = [FilePermission.FileListRequiredMixin, IsAuthenticated]
    # filter_fields = ('groups',)


class UtilsFileListByPageAPI(WebTokenAuthentication, generics.ListAPIView):
    module = models.FILE
    serializer_class = serializers.FileSerializer
    queryset = models.FILE.objects.all()
    permission_classes = [AllowAny, ]
    # permission_classes = [FilePermission.FileListRequiredMixin, IsAuthenticated]
    pagination_class = FilePagination


class UtilsFileCreateAPI(WebTokenAuthentication,generics.CreateAPIView):
    module = models.FILE
    serializer_class = serializers.FileSerializer
    permission_classes = [AllowAny, ]
    # permission_classes = [FilePermission.FileCreateRequiredMixin, IsAuthenticated]


class UtilsFileDeleteAPI(WebTokenAuthentication,generics.DestroyAPIView):
    module = models.FILE
    serializer_class = serializers.FileSerializer
    queryset = models.FILE.objects.all()
    permission_classes = [AllowAny, ]
    # permission_classes = [FilePermission.FileDeleteRequiredMixin, IsAuthenticated]
