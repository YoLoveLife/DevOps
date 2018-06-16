# -*- coding:utf-8 -*-
# !/usr/bin/env python
# Time 18-6-7
# Author Yo
# Email YoLoveLife@outlook.com
import datetime
import django_filters
from ops import models
from manager.models import Host
from django.db.models import Q

__all__ = [
    'MetaFilter',
            ]


class MetaFilter(django_filters.FilterSet):
    args = django_filters.CharFilter(method="args_filter")
    host = django_filters.CharFilter(method="host_filter")

    class Meta:
        model = models.META
        fields = ['group', 'args', 'host']

    @staticmethod
    def args_filter(queryset, first_name, value):
        contents = models.META_CONTENT.objects.filter(args__icontains=value)
        return queryset.filter(contents__in=contents)

    @staticmethod
    def host_filter(queryset, first_name, value):
        hosts = Host.objects.filter(Q(connect_ip__icontains=value)|Q(hostname__contains=value))
        return queryset.filter(hosts__in=hosts)