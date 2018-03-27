# -*- coding:utf-8 -*-
from .. import models
from .. import serializers
from rest_framework.views import Response,status
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated,AllowAny
from ..permission import meta as MetaPermission
from deveops.api import WebTokenAuthentication


class OpsMetaListAPI(WebTokenAuthentication,generics.ListAPIView):
    module = models.META
    serializer_class = serializers.MetaSerializer
    permission_classes = [MetaPermission.MetaListRequiredMixin,IsAuthenticated]
    # permission_classes = [AllowAny]

    # 所有運維工程師有如下特點
    # 1、僅能查看自己所管理的應用組
    # 2、可以增删改自己所管理的应用组的所有Meta操作
    def get_queryset(self):
        queryset = models.META.objects.filter(group__users__id=self.request.user.id)
        return queryset

