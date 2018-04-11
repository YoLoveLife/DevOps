# -*- coding:utf-8 -*-
from .. import models
from .. import serializers
from rest_framework.views import Response,status
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated,AllowAny
from ..permission import meta as MetaPermission
from deveops.api import WebTokenAuthentication
from rest_framework.pagination import PageNumberPagination

__all__ = [
    'MetaPagination', 'OpsMetaListAPI', 'OpsMetaListByPageAPI',
    'OpsMetaNeedFileCheckAPI', 'OpsMetaCreateAPI', 'OpsMetaDeleteAPI',
    'OpsMetaDirAPI', 'OpsMetaUpdateAPI'
]


class MetaPagination(PageNumberPagination):
    page_size = 10


class OpsMetaListAPI(WebTokenAuthentication,generics.ListAPIView):
    module = models.META
    serializer_class = serializers.MetaSerializer
    # permission_classes = [MetaPermission.MetaListRequiredMixin,IsAuthenticated]
    permission_classes = [AllowAny]
    filter_fields = ('group',)
    from rest_framework.renderers import JSONRenderer
    renderer_classes = [JSONRenderer,]

    def get_queryset(self):
        # queryset = models.META.objects.filter(group__users__id=self.request.user.id)
        queryset = models.META.objects.all()
        return queryset


class OpsMetaListByPageAPI(WebTokenAuthentication,generics.ListAPIView):
    module = models.META
    serializer_class = serializers.MetaSerializer
    permission_classes = [MetaPermission.MetaListRequiredMixin,IsAuthenticated]
    pagination_class = MetaPagination

    # 所有運維工程師有如下特點
    # 1、僅能查看自己所管理的應用組
    # 2、可以增删改自己所管理的应用组的所有Meta操作
    def get_queryset(self):
        # queryset = models.META.objects.filter(group__users__id=self.request.user.id)
        queryset = models.META.objects.all()
        return queryset


class OpsMetaCreateAPI(WebTokenAuthentication,generics.CreateAPIView):
    module = models.META
    serializer_class = serializers.MetaSerializer
    # permission_classes = [MetaPermission.MetaCreateRequiredMixin,IsAuthenticated]
    permission_classes = [AllowAny,]


class OpsMetaUpdateAPI(WebTokenAuthentication,generics.UpdateAPIView):
    module = models.META
    serializer_class = serializers.MetaSerializer
    queryset = models.META.objects.all()
    permission_classes = [MetaPermission.MetaUpdateRequiredMixin,IsAuthenticated]


class OpsMetaDeleteAPI(WebTokenAuthentication,generics.DestroyAPIView):
    module = models.META
    serializer_class = serializers.MetaSerializer
    queryset = models.META.objects.all()
    permission_classes = [MetaPermission.MetaDeleteRequiredMixin,IsAuthenticated]


class OpsMetaNeedFileCheckAPI(WebTokenAuthentication,generics.ListAPIView):
    module = models.META
    serializer_class = serializers.MetaNeedFileSerializer
    # permission_classes = [MetaPermission.MetaListRequiredMixin,IsAuthenticated]
    permission_classes = [AllowAny,]

    def get_queryset(self):
        return models.META.objects.filter(id=int(self.kwargs['pk']))

class OpsMetaDirAPI(WebTokenAuthentication,generics.UpdateAPIView):
    module = models.META
    serializer_class = serializers.OpsDirSerializer
    queryset = models.META.objects.all()
    # permission_classes = [GroupPermission.GroupUpdateRequiredMixin,IsAuthenticated]
    permission_classes = [AllowAny,]