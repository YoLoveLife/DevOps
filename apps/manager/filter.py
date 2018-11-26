# -*- coding:utf-8 -*-
# !/usr/bin/env python
# Time 18-6-7
# Author Yo
# Email YoLoveLife@outlook.com
import django_filters
from django.db.models import Q
from manager import models

__all__ = [
    'HostFilter', 'GroupFilter'
]


class HostFilter(django_filters.FilterSet):
    connect_ip = django_filters.CharFilter(method="connect_ip_filter")
    info = django_filters.CharFilter(method="info_filter")
    systype = django_filters.CharFilter(method="systype_filter")
    position = django_filters.CharFilter(method="position_filter")
    hostname = django_filters.CharFilter(method="hostname_filter")
    uuid = django_filters.CharFilter(method="uuid_filter")

    class Meta:
        model = models.Host
        fields = ['groups', 'connect_ip', 'hostname', 'sshport', 'info', 'systype', 'position', 'uuid']

    @staticmethod
    def connect_ip_filter(queryset, first_name, value):
        return queryset.filter(connect_ip__icontains=value)

    @staticmethod
    def info_filter(queryset, first_name, value):
        return queryset.filter(info__icontains=value)

    @staticmethod
    def systype_filter(queryset, first_name, value):
        return queryset.filter(systype__icontains=value)

    @staticmethod
    def position_filter(queryset, first_name, value):
        return queryset.filter(position__icontains=value)

    @staticmethod
    def hostname_filter(queryset, first_name, value):
        return queryset.filter(hostname__icontains=value)

    @staticmethod
    def uuid_filter(queryset, first_name, value):
        if '-' in value and len(value) == 36:
            import uuid
            return queryset.filter(uuid=uuid.UUID(value))
        else:
            return queryset


class GroupFilter(django_filters.FilterSet):
    info = django_filters.CharFilter(method="info_filter")
    ops = django_filters.CharFilter(method="ops_filter")
    status = django_filters.CharFilter(method="status_filter")
    instance_group = django_filters.CharFilter(method="instance_group_filter")
    uuid = django_filters.CharFilter(method="uuid_filter")

    class Meta:
        model = models.Group
        fields = ['info', 'ops', 'status', 'instance_group', 'uuid']

    @staticmethod
    def info_filter(queryset, first_name, value):
        return queryset.filter(Q(name__icontains=value)|Q(info__icontains=value))

    @staticmethod
    def ops_filter(queryset, first_name, value):
        users = models.ExtendUser.objects.filter(Q(full_name__icontains=value) | Q(username__icontains=value))
        return queryset.filter(users__in=users)

    @staticmethod
    def status_filter(queryset, first_name, value):
        return queryset.filter(_status=value)

    @staticmethod
    def instance_group_filter(queryset, first_name, value):
        return queryset.filter(dbgroup__isnull=True)

    @staticmethod
    def uuid_filter(queryset, first_name, value):
        if '-' in value and len(value) == 36:
            import uuid
            return queryset.filter(uuid=uuid.UUID(value))
        else:
            return queryset
