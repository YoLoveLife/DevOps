# -*- coding:utf-8 -*-
# !/usr/bin/env python
# Time 17-10-25
# Author Yo
# Email YoLoveLife@outlook.com
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.pagination import PageNumberPagination
from django.conf import settings
from deveops.api import WebTokenAuthentication
from authority.permission import group as GroupPermission
from timeline.decorator import decorator_api
from .. import models, serializers, filter

__all__ = [
    "GroupListAPI", "GroupCreateAPI", "GroupUpdateAPI",
    "GroupDeleteAPI", "GroupListByPageAPI",
    "GroupPagination",
]


class GroupPagination(PageNumberPagination):
    page_size = 10


class GroupListAPI(WebTokenAuthentication, generics.ListAPIView):
    module = models.Group
    serializer_class = serializers.GroupSerializer
    queryset = models.Group.objects.all()
    permission_classes = [GroupPermission.GroupListRequiredMixin, IsAuthenticated]
    filter_class = filter.GroupFilter


class GroupListByPageAPI(WebTokenAuthentication, generics.ListAPIView):
    module = models.Group
    serializer_class = serializers.GroupSerializer
    queryset = models.Group.objects.all().order_by('id')
    permission_classes = [GroupPermission.GroupListRequiredMixin, IsAuthenticated]
    pagination_class = GroupPagination
    filter_class = filter.GroupFilter


class GroupCreateAPI(WebTokenAuthentication, generics.CreateAPIView):
    module = models.Group
    serializer_class = serializers.GroupSerializer
    permission_classes = [GroupPermission.GroupCreateRequiredMixin, IsAuthenticated]
    msg = settings.LANGUAGE.GroupCreateAPI

    @decorator_api(timeline_type=settings.TIMELINE_KEY_VALUE['Permission_PMNGROUP_CREATE'])
    def create(self, request, *args, **kwargs):
        if self.qrcode_check(request):
            response = super(GroupCreateAPI, self).create(request, *args, **kwargs)
            return self.msg.format(
                USER=request.user.full_name,
                NAME=response.data['name'],
            ), response
        else:
            return '', self.qrcode_response


class GroupUpdateAPI(WebTokenAuthentication, generics.UpdateAPIView):
    module = models.Group
    serializer_class = serializers.GroupSerializer
    queryset = models.Group.objects.all()
    permission_classes = [GroupPermission.GroupUpdateRequiredMixin, IsAuthenticated]
    msg = settings.LANGUAGE.GroupUpdateAPI

    @decorator_api(timeline_type=settings.TIMELINE_KEY_VALUE['Permission_PMNGROUP_UPDATE'])
    def update(self, request, *args, **kwargs):
        if self.qrcode_check(request):
            response = super(GroupUpdateAPI, self).update(request, *args, **kwargs)
            pmngroup = self.get_object()
            return self.msg.format(
                USER=request.user.full_name,
                NAME=pmngroup.name,
            ), response
        else:
            return '', self.qrcode_response


class GroupDeleteAPI(WebTokenAuthentication, generics.DestroyAPIView):
    module = models.Group
    serializer_class = serializers.GroupSerializer
    queryset = models.Group.objects.all()
    permission_classes = [GroupPermission.GroupDeleteRequiredMixin, IsAuthenticated]
    msg = settings.LANGUAGE.GroupDeleteAPI

    @decorator_api(timeline_type=settings.TIMELINE_KEY_VALUE['Permission_PMNGROUP_DELETE'])
    def delete(self, request, *args, **kwargs):
        if self.qrcode_check(request):
            pmngroup = self.get_object()
            response = super(GroupDeleteAPI, self).delete(request, *args, **kwargs)
            return self.msg.format(
                USER=request.user.full_name,
                NAME=pmngroup.name,
            ), response
        else:
            return '', self.qrcode_response

