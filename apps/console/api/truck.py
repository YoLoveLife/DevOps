# -*- coding:utf-8 -*-
# !/usr/bin/env python
# Time 18-3-19
# Author Yo
# Email YoLoveLife@outlook.com
from .. import models, serializers, filter
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated,AllowAny
from rest_framework.pagination import PageNumberPagination
from rest_framework.views import Response, status
from ..permission import truck as TruckPermission
from deveops.api import WebTokenAuthentication
from rest_framework.views import APIView

__all__ = [

]


class ConsolePagination(PageNumberPagination):
    page_size = 10


class ConsoleTruckCreateAPI(WebTokenAuthentication, generics.CreateAPIView):
    module = models.Truck
    serializer_class = serializers.ConsoleTruckSerializer
    queryset = models.Truck.objects.all()
    permission_classes = [TruckPermission.TruckCreateRequiredMixin, IsAuthenticated]
