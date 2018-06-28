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