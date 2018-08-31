# -*- coding:utf-8 -*-
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated,AllowAny
from rest_framework.pagination import PageNumberPagination
from deveops.api import WebTokenAuthentication
from authority.permission import group as GroupPermission
from .. import models,serializers,filter

__all__ = [
    "GroupListAPI", "GroupCreateAPI", "GroupUpdateAPI",
    "GroupDeleteAPI", 'GroupListByPageAPI',
    "GroupPagination"
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


class GroupUpdateAPI(WebTokenAuthentication, generics.UpdateAPIView):
    module = models.Group
    serializer_class = serializers.GroupSerializer
    queryset = models.Group.objects.all()
    permission_classes = [GroupPermission.GroupUpdateRequiredMixin, IsAuthenticated]


class GroupDeleteAPI(WebTokenAuthentication, generics.DestroyAPIView):
    module = models.Group
    serializer_class = serializers.GroupSerializer
    queryset = models.Group.objects.all()
    permission_classes = [GroupPermission.GroupDeleteRequiredMixin, IsAuthenticated]

