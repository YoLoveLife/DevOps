# -*- coding:utf-8 -*-
from .. import models
from .. import serializers
from rest_framework.views import Response,status
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated,AllowAny
from ..permission import mission as MissionPermission
from deveops.api import WebTokenAuthentication
from rest_framework.pagination import PageNumberPagination

__all__ = [
    'MissionPagination', 'OpsMissionListAPI', 'OpsMissionListByPageAPI',
    'OpsMissionNeedFileCheckAPI', 'OpsMissionCreateAPI', 'OpsMissionDeleteAPI',
    'OpsMissionUpdateAPI'
]


class MissionPagination(PageNumberPagination):
    page_size = 10


class OpsMissionListAPI(WebTokenAuthentication,generics.ListAPIView):
    module = models.Mission
    serializer_class = serializers.MissionSerializer
    # permission_classes = [MissionPermission.MissionListRequiredMixin,IsAuthenticated]
    permission_classes = [AllowAny]

    def get_queryset(self):
        # queryset = models.Mission.objects.filter(group__users__id=self.request.user.id)
        queryset = models.Mission.objects.all()
        return queryset


class OpsMissionListByPageAPI(WebTokenAuthentication,generics.ListAPIView):
    module = models.Mission
    serializer_class = serializers.MissionSerializer
    permission_classes = [MissionPermission.MissionListRequiredMixin,IsAuthenticated]
    pagination_class = MissionPagination

    # 所有運維工程師有如下特點
    # 1、僅能查看自己所管理的應用組
    # 2、可以增删改自己所管理的应用组的所有Mission操作
    def get_queryset(self):
        # queryset = models.Mission.objects.filter(group__users__id=self.request.user.id)
        queryset = models.Mission.objects.all()
        return queryset


class OpsMissionCreateAPI(WebTokenAuthentication,generics.CreateAPIView):
    module = models.Mission
    serializer_class = serializers.MissionSerializer
    # permission_classes = [MissionPermission.MissionCreateRequiredMixin,IsAuthenticated]
    permission_classes = [AllowAny,]


class OpsMissionUpdateAPI(WebTokenAuthentication,generics.UpdateAPIView):
    module = models.Mission
    serializer_class = serializers.MissionSerializer
    queryset = models.Mission.objects.all()
    permission_classes = [MissionPermission.MissionUpdateRequiredMixin,IsAuthenticated]


class OpsMissionDeleteAPI(WebTokenAuthentication,generics.DestroyAPIView):
    module = models.Mission
    serializer_class = serializers.MissionSerializer
    queryset = models.Mission.objects.all()
    permission_classes = [MissionPermission.MissionDeleteRequiredMixin,IsAuthenticated]
