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
    host = django_filters.CharFilter(method="host_filter")
    info = django_filters.CharFilter(method="info_filter")
    uuid = django_filters.CharFilter(method="uuid_filter")

    class Meta:
        model = models.META
        fields = ['group', 'host', 'info', 'uuid']


    @staticmethod
    def host_filter(queryset, first_name, value):
        hosts = Host.objects.filter(Q(connect_ip__icontains=value) | Q(hostname__contains=value))
        return queryset.filter(hosts__in=hosts).distinct()

    @staticmethod
    def info_filter(queryset, first_name, value):
        return queryset.filter(info__icontains=value)

    @staticmethod
    def uuid_filter(queryset, first_name, value):
        if '-' in value and len(value) == 36:
            import uuid
            return queryset.filter(uuid=uuid.UUID(value))
        else:
            return queryset


class MissionFilter(django_filters.FilterSet):
    need_validate = django_filters.CharFilter(method="need_validate_filter")
    info = django_filters.CharFilter(method="info_filter")
    uuid = django_filters.CharFilter(method="uuid_filter")

    class Meta:
        model = models.Mission
        fields = ['need_validate', 'group', 'info', 'uuid']

    @staticmethod
    def need_validate_filter(queryset, first_name, value):
        return queryset.filter(need_validate=value)

    @staticmethod
    def info_filter(queryset, first_name, value):
        return queryset.filter(info__icontains=value)

    @staticmethod
    def uuid_filter(queryset, first_name, value):
        if '-' in value and len(value) == 36:
            import uuid
            return queryset.filter(uuid=uuid.UUID(value))
        else:
            return queryset