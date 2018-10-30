# -*- coding:utf-8 -*-
# !/usr/bin/env python
# Time 18-6-7
# Author Yo
# Email YoLoveLife@outlook.com
import datetime
import django_filters
from work import models
from ops.models import Push_Mission
from django.db.models import Q

__all__ = ['CodeWorkFilter',
            ]


class CodeWorkFilter(django_filters.FilterSet):
    time = django_filters.CharFilter(method="time_filter")
    user = django_filters.CharFilter(method="user_filter")
    info = django_filters.CharFilter(method="info_filter")

    class Meta:
        model = models.Code_Work
        fields = ['time', 'info', 'user']

    @staticmethod
    def time_filter(queryset, first_name, value):
        date_list = value.split('to')
        start_time = datetime.datetime.strptime(date_list[0],"%Y-%m-%d")
        end_time = datetime.datetime.strptime(date_list[1], "%Y-%m-%d")
        pm = Push_Mission.objects.filter(
            Q(create_time__range=(start_time,end_time))|Q(finish_time__range=(start_time,end_time))
        )
        return queryset.filter(push_mission__in=pm)

    @staticmethod
    def user_filter(queryset, first_name, value):
        users = models.ExtendUser.objects.filter(Q(full_name__icontains=value)|Q(username__icontains=value))
        return queryset.filter(user__in=users)

    @staticmethod
    def info_filter(queryset, first_name, value):
        return queryset.filter(info__icontains=value)


class SafeWorkFilter(django_filters.FilterSet):
    src_group = django_filters.CharFilter(method="src_group_filter")
    src_hosts = django_filters.CharFilter(method="src_hosts_filter")
    dest_group = django_filters.CharFilter(method="dest_group_filter")
    dest_hosts = django_filters.CharFilter(method="dest_hosts_filter")
    info = django_filters.CharFilter(method="info_filter")

    class Meta:
        model = models.Safe_Work
        fields = [
            'src_group' , 'src_hosts', 'info',
            'dest_group', 'dest_hosts', 'dest_port'
        ]

    @staticmethod
    def src_group_filter(queryset, first_name, value):
        group = models.Group.objects.filter(name__icontains=value)
        return queryset.filter(src_group=group)


    @staticmethod
    def src_hosts_filter(queryset, first_name, value):
        hosts = models.Host.objects.filter(
            Q(hostname__icontains=value)|Q(connect_ip__icontains=value)
        )
        return queryset.filter(src_hosts__in=hosts)


    @staticmethod
    def dest_group_filter(queryset, first_name, value):
        group = models.Group.objects.filter(name__icontains=value)
        return queryset.filter(dest_group=group)


    @staticmethod
    def dest_hosts_filter(queryset, first_name, value):
        hosts = models.Host.objects.filter(
            Q(hostname__icontains=value)|Q(connect_ip__icontains=value)
        )
        return queryset.filter(dest_hosts__in=hosts)


    @staticmethod
    def info_filter(queryset, first_name, value):
        return queryset.filter(
            Q(src_info__icontains=value)|Q(dest_info__icontains=value)
        )
