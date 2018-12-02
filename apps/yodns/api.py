# -*- coding:utf-8 -*-
# !/usr/bin/env python
# Time 18-3-19
# Author Yo
# Modify WZZ
# Email YoLoveLife@outlook.com
from rest_framework.permissions import IsAuthenticated,AllowAny
from rest_framework.pagination import PageNumberPagination
from rest_framework.views import Response, status
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework import filters
from rest_framework import generics, mixins, views
from rest_framework.viewsets import GenericViewSet
from deveops.api import WebTokenAuthentication
from yodns import permission as DNSPermission
from yodns import models,serializers,filter

__all__ = [

]

class DNSPagination(PageNumberPagination):
    page_size = 10



class DNSListAPI(WebTokenAuthentication, generics.ListAPIView):
    '''
        无分页列出所有DNS列表
    '''
    module = models.DNS
    serializer_class = serializers.DNSSerializer
    queryset = models.DNS.objects.all()
    permission_classes = [DNSPermission.DNSListRequiredMixin, IsAuthenticated]
    filter_class = filter.DNSFilter


class DNSListByPageAPI(DNSListAPI):
    pagination_class = DNSPagination


class DNSCreateAPI(WebTokenAuthentication, generics.CreateAPIView):
    module = models.DNS
    serializer_class = serializers.DNSSerializer
    queryset = models.DNS.objects.all()
    permission_classes = [DNSPermission.DNSCreateRequiredMixin, IsAuthenticated]


class DNSUpdateAPI(WebTokenAuthentication, generics.UpdateAPIView):
    module = models.DNS
    serializer_class = serializers.DNSSerializer
    queryset = models.DNS.objects.all()
    permission_classes = [DNSPermission.DNSUpdateRequiredMixin, IsAuthenticated]
    lookup_url_kwarg = 'pk'
    lookup_field = 'uuid'


class DNSDeleteAPI(WebTokenAuthentication, generics.DestroyAPIView):
    module = models.DNS
    serializer_class = serializers.DNSSerializer
    queryset = models.DNS.objects.all()
    permission_classes = [DNSPermission.DNSDeleteRequiredMixin, IsAuthenticated]
    lookup_url_kwarg = 'pk'
    lookup_field = 'uuid'
