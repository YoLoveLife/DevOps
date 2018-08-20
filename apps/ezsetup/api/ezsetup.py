# -*- coding:utf-8 -*-
# !/usr/bin/env python
# Time 18-3-19
# Author Yo
# Email YoLoveLife@outlook.com
from ezsetup import models,serializers
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated,AllowAny
from deveops.api import WebTokenAuthentication
from rest_framework.pagination import PageNumberPagination
from rest_framework.views import Response, status

__all__ = [

]

class EZSetupPagination(PageNumberPagination):
    page_size = 10


class EZSetupListByPageAPI(WebTokenAuthentication, generics.ListAPIView):
    module = models.SETUP
    serializer_class = serializers.EZSetupSerializer
    queryset = models.SETUP.objects.all()
    # permission_classes = [InstancePermission.DBInstanceListRequiredMixin, IsAuthenticated]
    permission_classes = [AllowAny,]
    pagination_class = EZSetupPagination


class EZSetupCreateRedisAPI(WebTokenAuthentication, generics.CreateAPIView):
    module = models.SETUP
    serializer_class = serializers.EZSetupRedisSerializer
    queryset = models.SETUP.objects.all()
    permission_classes = [AllowAny,]
