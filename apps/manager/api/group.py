# -*- coding:utf-8 -*-
# !/usr/bin/env python
# Time 18-3-19
# Author Yo
# Email YoLoveLife@outlook.com
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.pagination import PageNumberPagination
from rest_framework.views import Response, status
from django.conf import settings
from deveops.api import WebTokenAuthentication
from timeline.decorator import decorator_api
from manager.permission import group as GroupPermission
from .. import models, serializers, filter

__all__ = [
    'ManagerGroupListAPI', 'ManagerGroupCreateAPI', 'ManagerGroupDetailAPI',
    'ManagerGroupUpdateAPI', 'ManagerGroupDeleteAPI',
    'GroupPagination', 'ManagerGroupListByPageAPI'
]


class ManagerGroupListAPI(WebTokenAuthentication, generics.ListAPIView):
    module = models.Group
    serializer_class = serializers.GroupSampleSerializer
    queryset = models.Group.objects.all()
    permission_classes = [GroupPermission.GroupListRequiredMixin, IsAuthenticated]
    filter_class = filter.GroupFilter


class ManagerGroupListByOpsAPI(WebTokenAuthentication, generics.ListAPIView):
    module = models.Group
    serializer_class = serializers.GroupSerializer
    permission_classes = [GroupPermission.GroupListRequiredMixin, IsAuthenticated]
    filter_class = filter.GroupFilter

    def get_queryset(self):
        user = self.request.user
        return user.assetgroups.all()


class GroupPagination(PageNumberPagination):
    page_size = 10


class ManagerGroupListByPageAPI(WebTokenAuthentication, generics.ListAPIView):
    module = models.Group
    serializer_class = serializers.GroupSerializer
    queryset = models.Group.objects.all()
    permission_classes = [GroupPermission.GroupListRequiredMixin, IsAuthenticated]
    pagination_class = GroupPagination
    filter_class = filter.GroupFilter


class ManagerGroupCreateAPI(WebTokenAuthentication, generics.CreateAPIView):
    module = models.Group
    serializer_class = serializers.GroupSerializer
    permission_classes = [GroupPermission.GroupCreateRequiredMixin, IsAuthenticated]
    msg = settings.LANGUAGE.ManagerGroupCreateAPI

    @decorator_api(timeline_type=settings.TIMELINE_KEY_VALUE['Group_GROUP_CREATE'])
    def create(self, request, *args, **kwargs):
        if self.qrcode_check(request):
            response = super(ManagerGroupCreateAPI, self).create(request, *args, **kwargs)
            return self.msg.format(
                USER=request.user.full_name,
                NAME=response.data['name'],
                UUID=response.data['uuid'],
            ), response
        else:
            return '', self.qrcode_response


class ManagerGroupDetailAPI(WebTokenAuthentication, generics.ListAPIView):
    module = models.Group
    serializer_class = serializers.GroupSerializer
    permission_classes = [GroupPermission.GroupDetailRequiredMixin, IsAuthenticated]

    def get_queryset(self):
        return models.Group.objects.filter(id=int(self.kwargs['pk']))


class ManagerGroupUpdateAPI(WebTokenAuthentication, generics.UpdateAPIView):
    module = models.Group
    serializer_class = serializers.GroupSerializer
    queryset = models.Group.objects.all()
    permission_classes = [GroupPermission.GroupUpdateRequiredMixin, IsAuthenticated]
    lookup_field = 'uuid'
    lookup_url_kwarg = 'pk'
    msg = settings.LANGUAGE.ManagerGroupUpdateAPI

    @decorator_api(timeline_type=settings.TIMELINE_KEY_VALUE['Group_GROUP_UPDATE'])
    def update(self, request, *args, **kwargs):
        if self.qrcode_check(request):
            response = super(ManagerGroupUpdateAPI, self).update(request, *args, **kwargs)
            group = self.get_object()
            return self.msg.format(
                USER=request.user.full_name,
                NAME=group.name,
                UUID=group.uuid
            ), response
        else:
            return '', self.qrcode_response


class ManagerGroupDeleteAPI(WebTokenAuthentication, generics.DestroyAPIView):
    module = models.Group
    serializer_class = serializers.GroupSerializer
    queryset = models.Group.objects.all()
    permission_classes = [GroupPermission.GroupDeleteRequiredMixin, IsAuthenticated]
    lookup_field = 'uuid'
    lookup_url_kwarg = 'pk'
    msg = settings.LANGUAGE.ManagerGroupDeleteAPI

    @decorator_api(timeline_type=settings.TIMELINE_KEY_VALUE['Group_GROUP_DELETE'])
    def delete(self, request, *args, **kwargs):
        if self.qrcode_check(request):
            group = self.get_object()
            if group.hosts.count() != 0:
                return self.msg.format(
                    USER=request.user.full_name,
                    NAME=group.name,
                    UUID=group.uuid
                ), Response({
                    'detail': settings.LANGUAGE.ManagerGroupDeleteAPIExsistHost
                }, status=status.HTTP_406_NOT_ACCEPTABLE)
            else:
                return self.msg.format(
                    USER=request.user.full_name,
                    NAME=group.name,
                    UUID=group.uuid
                ), super(ManagerGroupDeleteAPI, self).delete(request, *args, **kwargs)
        else:
            return '', self.qrcode_response


class ManagerGroupSelectHostAPI(WebTokenAuthentication, generics.UpdateAPIView):
    module = models.Group
    serializer_class = serializers.GroupSelectHostSerializer
    queryset = models.Group.objects.all()
    permission_classes = [GroupPermission.GroupSelectHostRequiredMixin, IsAuthenticated]
    msg = settings.LANGUAGE.ManagerGroupSelectHostAPI

    @decorator_api(timeline_type=settings.TIMELINE_KEY_VALUE['Group_GROUP_SORT'])
    def update(self, request, *args, **kwargs):
        if self.qrcode_check(request):
            group = self.get_object()
            response = super(ManagerGroupSelectHostAPI, self).update(request, *args, **kwargs)
            return self.msg.format(
                USER=request.user.full_name,
                NAME=group.name,
                UUID=group.uuid
            ), response
        else:
            return '', self.qrcode_response

