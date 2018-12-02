# -*- coding:utf-8 -*-
# !/usr/bin/env python
# Time 18-3-19
# Author Yo
# Email YoLoveLife@outlook.com
from yocdn import models,serializers,filter
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated,AllowAny
from rest_framework.pagination import PageNumberPagination
from rest_framework.views import Response, status
from django.conf import settings
from rest_framework import generics
from deveops.api import WebTokenAuthentication
from timeline.decorator import decorator_api
__all__ = [

]


class YoCDNPagination(PageNumberPagination):
    page_size = 10


class YoCDNListByPageAPI(WebTokenAuthentication, generics.ListAPIView):
    module = models.CDN
    serializer_class = serializers.YoCDNSerializer
    queryset = models.CDN.objects.all().order_by('-id')
    permission_classes = [AllowAny,]
    pagination_class = YoCDNPagination
    filter_class = filter.CDNFilter


class YoCDNCreateAPI(WebTokenAuthentication, generics.CreateAPIView):
    module = models.CDN
    serializer_class = serializers.YoCDNListSerializer
    permission_classes = [AllowAny,]
    msg = settings.LANGUAGE.YoCDNCreateAPI

    @decorator_api(timeline_type=settings.TIMELINE_KEY_VALUE['CDN_CDN_CREATE'])
    def create(self, request, *args, **kwargs):
        response = super(YoCDNCreateAPI, self).create(request, *args, **kwargs)
        return self.msg.format(
            USER = request.user.full_name
        ), response