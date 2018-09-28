# -*- coding:utf-8 -*-
from .. import models, serializers, filter
from rest_framework.views import Response,status
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated,AllowAny
from ..permission import meta as MetaPermission
from django.conf import settings
from deveops.api import WebTokenAuthentication
from rest_framework.pagination import PageNumberPagination
from timeline.decorator import decorator_api

__all__ = [
    'MetaPagination', 'OpsMetaListAPI', 'OpsMetaListByPageAPI',
    'OpsMetaCreateAPI', 'OpsMetaDeleteAPI',
    'OpsMetaUpdateAPI',
]


class MetaPagination(PageNumberPagination):
    page_size = 10


class OpsMetaListAPI(WebTokenAuthentication, generics.ListAPIView):
    module = models.META
    serializer_class = serializers.MetaSerializer
    permission_classes = [MetaPermission.MetaListRequiredMixin, IsAuthenticated]
    filter_class = filter.MetaFilter

    def get_queryset(self):
        user = self.request.user
        groups = models.Group.objects.filter(users=user)
        queryset = models.META.objects.filter(group_id__in=groups)
        return queryset


class OpsMetaListByPageAPI(WebTokenAuthentication, generics.ListAPIView):
    module = models.META
    serializer_class = serializers.MetaSerializer
    permission_classes = [MetaPermission.MetaListRequiredMixin, IsAuthenticated]
    pagination_class = MetaPagination
    filter_class = filter.MetaFilter
    # 所有運維工程師有如下特點
    # 1、僅能查看自己所管理的應用組
    # 2、可以增删改自己所管理的应用组的所有Meta操作

    def get_queryset(self):
        user = self.request.user
        groups = models.Group.objects.filter(users=user)
        queryset = models.META.objects.filter(group_id__in=groups)
        return queryset


class OpsMetaCreateAPI(WebTokenAuthentication, generics.CreateAPIView):
    module = models.META
    serializer_class = serializers.MetaSerializer
    permission_classes = [MetaPermission.MetaCreateRequiredMixin, IsAuthenticated]
    msg = settings.LANGUAGE.OpsMetaCreateAPI

    # 校验用户QR-Code
    @decorator_api(timeline_type = settings.TIMELINE_KEY_VALUE['META_META_CREATE'])
    def create(self, request, *args, **kwargs):

        if 'qrcode' in request.data.keys() and self.request.user.check_qrcode(request.data.get('qrcode')):
            response = super(OpsMetaCreateAPI, self).create(request, *args, **kwargs)
            return self.msg.format(
                USER = request.user.full_name,
                UUID = response.data['uuid'],
            ), response

        else:
            response = Response({'detail': '您的QR-Code有误'}, status=status.HTTP_406_NOT_ACCEPTABLE)
            return '', response


class OpsMetaUpdateAPI(WebTokenAuthentication, generics.UpdateAPIView):
    module = models.META
    serializer_class = serializers.MetaSerializer
    queryset = models.META.objects.all()
    permission_classes = [MetaPermission.MetaUpdateRequiredMixin, IsAuthenticated]
    lookup_field = 'uuid'
    lookup_url_kwarg = 'pk'
    msg = settings.LANGUAGE.OpsMetaUpdateAPI

    @decorator_api(timeline_type = settings.TIMELINE_KEY_VALUE['META_META_UPDATE'])
    def update(self, request, *args, **kwargs):
        meta = self.get_object()
        if 'qrcode' in request.data.keys() and self.request.user.check_qrcode(request.data.get('qrcode')):
            response = super(OpsMetaUpdateAPI, self).update(request, *args, **kwargs)
            return self.msg.format(
                USER = request.user.full_name,
                UUID = meta.uuid,
                INFO = meta.info,
            ), response
        else:
            response = Response({'detail': '您的QR-Code有误'}, status=status.HTTP_406_NOT_ACCEPTABLE)
            return '', response


class OpsMetaDeleteAPI(WebTokenAuthentication, generics.DestroyAPIView):
    module = models.META
    serializer_class = serializers.MetaSerializer
    queryset = models.META.objects.all()
    permission_classes = [MetaPermission.MetaDeleteRequiredMixin, IsAuthenticated]
    lookup_field = 'uuid'
    lookup_url_kwarg = 'pk'
    msg = settings.LANGUAGE.OpsMetaDeleteAPI

    @decorator_api(timeline_type = settings.TIMELINE_KEY_VALUE['META_META_DELETE'])
    def delete(self, request, *args, **kwargs):
        meta = self.get_object()
        if 'qrcode' in request.data.keys() and self.request.user.check_qrcode(request.data.get('qrcode')):
            response = super(OpsMetaDeleteAPI, self).delete(request, *args, **kwargs)
            return self.msg.format(
                USER=request.user.full_name,
                UUID=meta.uuid,
                INFO=meta.info,
            ),response
        else:
            response = Response({'detail': '您的QR-Code有误'}, status=status.HTTP_406_NOT_ACCEPTABLE)
            return '', response







