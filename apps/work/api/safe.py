# -*- coding:utf-8 -*-
# !/usr/bin/env python
# Time 18-3-19
# Author Yo
# Email YoLoveLife@outlook.com
from .. import models, serializers,filter
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated,AllowAny
from rest_framework.pagination import PageNumberPagination
from rest_framework.views import Response, status
from ..permission import safework as SafeWorkPermission
from deveops.api import WebTokenAuthentication
from rest_framework.views import APIView

__all__ = [

]


class SafeWorkPagination(PageNumberPagination):
    page_size = 10


class SafeWorkListByPageAPI(WebTokenAuthentication, generics.ListAPIView):
    module = models.Safe_Work
    serializer_class = serializers.SafeWorkSerializer
    queryset = models.Safe_Work.objects.all().order_by('-id')
    permission_classes = [SafeWorkPermission.SafeWorkListRequiredMixin, IsAuthenticated]
    pagination_class = SafeWorkPagination
    filter_class = filter.SafeWorkFilter


class SafeWorkCreateAPI(WebTokenAuthentication, generics.CreateAPIView):
    module = models.Safe_Work
    serializer_class = serializers.SafeWorkSerializer
    permission_classes = [SafeWorkPermission.SafeWorkCreateRequiredMixin, IsAuthenticated]


class SafeWorkStatusAPI(WebTokenAuthentication, generics.UpdateAPIView):
    module = models.Safe_Work
    serializer_class = serializers.SafeWorkStatusSerializer
    permission_classes = [SafeWorkPermission.SafeWorkStatusRequiredMixin, IsAuthenticated]
    queryset = models.Safe_Work.objects.all()
    lookup_url_kwarg = 'pk'
    lookup_field = 'uuid'