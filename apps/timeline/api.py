# -*- coding:utf-8 -*-
# !/usr/bin/env python
# Time 18-3-19
# Author Yo
# Email YoLoveLife@outlook.com
from timeline import models, serializers
from rest_framework import generics
from rest_framework.pagination import PageNumberPagination
from rest_framework.views import Response, status
from rest_framework.permissions import IsAuthenticated,AllowAny
from deveops.api import WebTokenAuthentication

__all__ = [
    'TimeLineListByPageAPI',
]

class TimeLinePagination(PageNumberPagination):
    page_size = 6


class TimeLineListByPageAPI(WebTokenAuthentication,generics.ListAPIView):
    module = models.History
    serializer_class = serializers.HistorySerializer
    permission_classes = [AllowAny, ]
    pagination_class = TimeLinePagination
    queryset = models.History.objects.all().order_by('-time')