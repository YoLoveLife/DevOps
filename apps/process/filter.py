# -*- coding:utf-8 -*-
# !/usr/bin/env python
# Time 18-6-7
# Author Yo
# Email YoLoveLife@outlook.com
import datetime
import django_filters
from yocdn import models
from django.db.models import Q

__all__ = [
    'CDNFilter',
]


class CDNFilter(django_filters.FilterSet):
    url = django_filters.CharFilter(method="url_filter")
    create_time = django_filters.CharFilter(method="time_filter")

    class Meta:
        model = models.CDN
        fields = ['url', 'type', 'status', 'create_time']

    @staticmethod
    def url_filter(queryset, first_name, value):
        return queryset.filter(url__icontains=value)


    @staticmethod
    def time_filter(queryset, first_name, value):
        date_list = value.split('to')
        start_time = datetime.datetime.strptime(date_list[0],"%Y-%m-%d")
        end_time = datetime.datetime.strptime(date_list[1], "%Y-%m-%d")

        pm = models.objects.filter(
            Q(create_time__range=(start_time,end_time))|Q(finish_time__range=(start_time,end_time))
        )
        return queryset.filter(push_mission__in=pm)