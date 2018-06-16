# -*- coding:utf-8 -*-
from .. import models, serializers, filter
from rest_framework.views import Response,status
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated,AllowAny
from ..permission import meta as MetaPermission
from deveops.api import WebTokenAuthentication
from rest_framework.pagination import PageNumberPagination

__all__ = [
    'MetaPagination', 'OpsMetaListAPI', 'OpsMetaListByPageAPI',
    'OpsMetaCreateAPI', 'OpsMetaDeleteAPI',
    'OpsMetaDirAPI', 'OpsMetaUpdateAPI'
]


class MetaPagination(PageNumberPagination):
    page_size = 10


class OpsMetaListAPI(WebTokenAuthentication,generics.ListAPIView):
    module = models.META
    serializer_class = serializers.MetaSerializer
    # permission_classes = [MetaPermission.MetaListRequiredMixin,IsAuthenticated]
    filter_class = filter.MetaFilter
    queryset = models.META.objects.all()
    # queryset = models.META.objects.filter(group__users__id=self.request.user.id)


class OpsMetaListByPageAPI(WebTokenAuthentication,generics.ListAPIView):
    module = models.META
    serializer_class = serializers.MetaSerializer
    # permission_classes = [MetaPermission.MetaListRequiredMixin,IsAuthenticated]
    queryset = models.META.objects.all()
    # queryset = models.META.objects.filter(group__users__id=self.request.user.id)
    pagination_class = MetaPagination
    filter_class = filter.MetaFilter
    # 所有運維工程師有如下特點
    # 1、僅能查看自己所管理的應用組
    # 2、可以增删改自己所管理的应用组的所有Meta操作


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
    lookup_field = 'uuid'
    lookup_url_kwarg = 'pk'


class OpsMetaDeleteAPI(WebTokenAuthentication,generics.DestroyAPIView):
    module = models.META
    serializer_class = serializers.MetaSerializer
    queryset = models.META.objects.all()
    permission_classes = [MetaPermission.MetaDeleteRequiredMixin,IsAuthenticated]
    lookup_field = 'uuid'
    lookup_url_kwarg = 'pk'
