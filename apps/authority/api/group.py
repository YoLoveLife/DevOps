# -*- coding:utf-8 -*-
from .. import models,serializers
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination
from rest_framework.views import Response,status
from rest_framework_jwt.views import ObtainJSONWebToken
from deveops.api import WebTokenAuthentication
from authority.permission import group as GroupPermission

__all__ = [
    "GroupListAPI", "GroupCreateAPI", "GroupUpdateAPI",
    "GroupDeleteAPI",
    "GroupPagination"
]


class GroupPagination(PageNumberPagination):
    page_size = 10


class GroupListAPI(generics.ListAPIView):
    module = models.Group
    serializer_class =serializers.GroupSerializer
    queryset = models.Group.objects.all()
    permission_classes = [GroupPermission.GroupListRequiredMixin,IsAuthenticated]
    # pagination_class = GroupPagination


class GroupCreateAPI(generics.CreateAPIView):
    module = models.Group
    serializer_class =serializers.GroupSerializer
    permission_classes = [GroupPermission.GroupCreateRequiredMixin,IsAuthenticated]


class GroupUpdateAPI(generics.UpdateAPIView):
    module = models.Group
    serializer_class = serializers.GroupSerializer
    queryset = models.Group.objects.all()
    permission_classes = [GroupPermission.GroupUpdateRequiredMixin,IsAuthenticated]


class GroupDeleteAPI(generics.DestroyAPIView):
    module =models.Group
    serializer_class = serializers.GroupSerializer
    queryset = models.Group.objects.all()
    permission_classes = [GroupPermission.GroupDeleteRequiredMixin,IsAuthenticated]


