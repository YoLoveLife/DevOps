# -*- coding:utf-8 -*-
# !/usr/bin/env python
# Time 18-6-7
# Author Yo
# Email YoLoveLife@outlook.com
import django_filters
from yodns import models
from django.db.models import Q

__all__ = ['DNSFilter',
            ]


from django_filters import filters



class DNSFilter(django_filters.FilterSet):

    url = django_filters.CharFilter(method="url_filter")
    internal_dig = django_filters.CharFilter(method="internal_dig_filter")
    external_dig = django_filters.CharFilter(method="external_dig_filter")

    class Meta:
        model = models.DNS
        fields = ['url', 'internal_dig', 'external_dig']


    @staticmethod
    def internal_dig_filter(queryset, first_name, value):
        return queryset.filter(internal_dig__icontains=value)


    @staticmethod
    def external_dig_filter(queryset, first_name, value):
        return queryset.filter(external_dig__icontains=value)


    @staticmethod
    def url_filter(queryset, first_name, value):
        return queryset.filter(url__icontains=value)

