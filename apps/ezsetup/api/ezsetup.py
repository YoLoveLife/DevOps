# -*- coding:utf-8 -*-
# !/usr/bin/env python
# Time 18-3-19
# Author Yo
# Email YoLoveLife@outlook.com
from ezsetup import models, serializers
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.conf import settings
from deveops.api import WebTokenAuthentication
from rest_framework.pagination import PageNumberPagination
from timeline.decorator import decorator_api

__all__ = [
    'EZSetupPagination', 'EZSetupCreateRedisAPI', 'EZSetupListByPageAPI',
]


class EZSetupPagination(PageNumberPagination):
    page_size = 10


class EZSetupListByPageAPI(WebTokenAuthentication, generics.ListAPIView):
    module = models.SETUP
    serializer_class = serializers.EZSetupSerializer
    queryset = models.SETUP.objects.all()
    permission_classes = [AllowAny, ]
    pagination_class = EZSetupPagination


class EZSetupCreateRedisAPI(WebTokenAuthentication, generics.CreateAPIView):
    module = models.SETUP
    serializer_class = serializers.EZSetupRedisSerializer
    queryset = models.SETUP.objects.all()
    permission_classes = [AllowAny, ]
    msg = settings.LANGUAGE.EZSetupCreateRedisAPI

    @decorator_api(timeline_type=settings.TIMELINE_KEY_VALUE['SETUP_REDIS_CREATE'])
    def create(self, request, *args, **kwargs):
        if self.qrcode_check(request):
            response = super(EZSetupCreateRedisAPI, self).create(request, *args, **kwargs)
            return self.msg.format(
                USER=request.user.full_name,
                UUID=response.data['uuid'],
            ), response
        else:
            return '', self.qrcode_response
