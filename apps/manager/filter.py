# -*- coding:utf-8 -*-
# !/usr/bin/env python
# Time 18-6-7
# Author Yo
# Email YoLoveLife@outlook.com
import django_filters
from manager import models
from django.db.models import Q

__all__ = ['HostFilter',
            ]


class HostFilter(django_filters.FilterSet):
    connect_ip = django_filters.CharFilter(method="connect_ip_filter")
    info = django_filters.CharFilter(method="info_filter")
    systype = django_filters.CharFilter(method="systype_filter")
    position = django_filters.CharFilter(method="position_filter")
    hostname = django_filters.CharFilter(method="hostname_filter")
    dbinstance = django_filters.CharFilter(method="dbinstance_filter")

    class Meta:
        model = models.Host
        fields = ['groups', 'connect_ip', 'hostname', 'sshport', 'info', 'systype', 'position', 'dbinstance']

    @staticmethod
    def connect_ip_filter(queryset, first_name, value):
        return queryset.filter(connect_ip__icontains=value)

    @staticmethod
    def info_filter(queryset, first_name, value):
        details = models.HostDetail.objects.filter(info__icontains=value)
        return queryset.filter(detail__in=details)

    @staticmethod
    def systype_filter(queryset, first_name, value):
        systype = models.System_Type.objects.filter(name__icontains=value)
        detail = models.HostDetail.objects.filter(systemtype__in=systype)
        return queryset.filter(detail__in=detail)

    @staticmethod
    def position_filter(queryset, first_name, value):
        position = models.Position.objects.filter(name__icontains=value)
        details = models.HostDetail.objects.filter(position__in=position)
        return queryset.filter(detail__in=details)

    @staticmethod
    def hostname_filter(queryset, first_name, value):
        return queryset.filter(hostname__icontains=value)

    @staticmethod
    def dbinstance_filter(queryset, first_name, value):
        return queryset.filter(dbinstance__isnull=True)


class GroupFilter(django_filters.FilterSet):
    info = django_filters.CharFilter(method="info_filter")
    ops = django_filters.CharFilter(method="ops_filter")
    status = django_filters.CharFilter(method="status_filter")
    instance_group = django_filters.CharFilter(method="instance_group_filter")

    class Meta:
        model = models.Group
        fields = ['info', 'ops', 'status', 'instance_group']

    @staticmethod
    def info_filter(queryset, first_name, value):
        return queryset.filter(Q(name__icontains=value)|Q(info__icontains=value))

    @staticmethod
    def ops_filter(queryset, first_name, value):
        users = models.ExtendUser.objects.filter(Q(full_name__icontains=value)|Q(username__icontains=value))
        return queryset.filter(users__in=users)

    @staticmethod
    def status_filter(queryset, first_name, value):
        return queryset.filter(_status=value)

    @staticmethod
    def instance_group_filter(queryset, first_name, value):
        return queryset.filter(dbgroup__isnull=True)