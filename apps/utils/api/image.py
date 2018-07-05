# -*- coding:utf-8 -*-
# !/usr/bin/env python
# Time 18-3-19
# Author Yo
# Email YoLoveLife@outlook.com
from .. import models, serializers
from django.conf import settings
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated,AllowAny
from rest_framework.pagination import PageNumberPagination
from rest_framework.views import Response, status
from utils.permission import image as ImagePermission
from deveops.api import WebTokenAuthentication

__all__ = [
    'ImagePagination', 'UtilsImageCreateAPI',
    'UtilsImageListAPI', 'UtilsImageListByPageAPI',
    'UtilsImageDeleteAPI',
]


class ImagePagination(PageNumberPagination):
    page_size = 10


class UtilsImageListAPI(WebTokenAuthentication,generics.ListAPIView):
    module = models.FILE
    serializer_class = serializers.ImageSerializer
    queryset = models.FILE.objects.all()
    permission_classes = [ImagePermission.ImageListRequiredMixin, IsAuthenticated]


class UtilsImageListByPageAPI(WebTokenAuthentication, generics.ListAPIView):
    module = models.FILE
    serializer_class = serializers.ImageSerializer
    permission_classes = [ImagePermission.ImageListRequiredMixin, IsAuthenticated]
    pagination_class = ImagePagination
    queryset = models.FILE.objects.all()


class UtilsImageCreateAPI(WebTokenAuthentication, generics.CreateAPIView):
    module = models.FILE
    serializer_class = serializers.ImageSerializer
    permission_classes = [ImagePermission.ImageCreateRequiredMixin, IsAuthenticated]


class UtilsImageDeleteAPI(WebTokenAuthentication, generics.DestroyAPIView):
    module = models.FILE
    serializer_class = serializers.ImageSerializer
    queryset = models.FILE.objects.all()
    permission_classes = [ImagePermission.ImageDeleteRequiredMixin, IsAuthenticated]
    lookup_field = 'uuid'
    lookup_url_kwarg = 'pk'

