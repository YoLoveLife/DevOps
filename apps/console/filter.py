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
    'MetaFilter', 'MissionFilter'
            ]


class MetaFilter(django_filters.FilterSet):
    args = django_filters.CharFilter(method="args_filter")
    host = django_filters.CharFilter(method="host_filter")
    mdle = django_filters.CharFilter(method="module_filter")

    class Meta:
        model = models.META
        fields = ['group', 'args', 'host', 'mdle']

    @staticmethod
    def args_filter(queryset, first_name, value):
        contents = models.META_CONTENT.objects.filter(args__icontains=value)
        return queryset.filter(contents__in=contents)

    @staticmethod
    def host_filter(queryset, first_name, value):
        hosts = Host.objects.filter(Q(connect_ip__icontains=value)|Q(hostname__contains=value))
        return queryset.filter(hosts__in=hosts)

    @staticmethod
    def module_filter(queryset, first_name, value):
        contents = models.META_CONTENT.objects.filter(module__icontains=value)
        return queryset.filter(contents__in=contents)


class MissionFilter(django_filters.FilterSet):
    need_validate = django_filters.CharFilter(method="need_validate_filter")
    info = django_filters.CharFilter(method="info_filter")

    class Meta:
        model = models.Mission
        fields = ['need_validate', 'group', 'info']

    @staticmethod
    def need_validate_filter(queryset, first_name, value):
        return queryset.filter(need_validate=value)

    @staticmethod
    def info_filter(queryset, first_name, value):
        return queryset.filter(info__icontains=value)