# -*- coding:utf-8 -*-
# !/usr/bin/env python
# Time 18-4-28
# Author Yo
# Email YoLoveLife@outlook.com
from .. import models, serializers
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated,AllowAny
from rest_framework.pagination import PageNumberPagination
from rest_framework.views import Response, status
# from variable.permission import var2group as Var2GroupPermission
from deveops.api import WebTokenAuthentication


class VariablePagination(PageNumberPagination):
    page_size = 10


class Variable2GroupListAPI(WebTokenAuthentication,generics.ListAPIView):
    module = models.Var2Group
    queryset = models.Var2Group.objects.all()
    serializer_class = serializers.Var2GroupSerializer
    permission_classes = [AllowAny,]
    filter_fields = '__all__'


class Variable2GroupCreateAPI(WebTokenAuthentication, generics.CreateAPIView):
    module = models.Var2Group
    serializer_class = serializers.Var2GroupSerializer
    permission_classes = [AllowAny,]


class Variable2GroupDeleteAPI(WebTokenAuthentication,generics.DestroyAPIView):
    module = models.Var2Group
    serializer_class = serializers.Var2GroupSerializer
    queryset = models.Var2Group.objects.all()
    permission_classes = [AllowAny,]
