# -*- coding:utf-8 -*-
# !/usr/bin/env python
# Time 18-6-7
# Author Yo
# Email YoLoveLife@outlook.com
import django_filters
from dns import models
from django.db.models import Q

__all__ = ['DNSFilter',
            ]


class DNSFilter(django_filters.FilterSet):
    dns_name = django_filters.CharFilter(method="dnsname_filter")
    level = django_filters.CharFilter(method="level_filter")
    class Meta:
        model = models.DNS
        fields = ['group', 'dns_name', 'inner_dig', 'dig',]

    @staticmethod
    def dnsname_filter(queryset, first_name, value):
        return queryset.filter(Q(father__name=value)|Q(father__father__name=value)|Q(name=value))

    @staticmethod
    def level_filter(queryset, first_name, value):
        if value == '1':
            return queryset.filter(father__isnull=True)
        elif value == '2':
            return queryset.filter(Q(father__father__isnull=True) & ~Q(father__isnull=True))
        else:
            return queryset.exclude(Q(father__isnull=True) | Q(father__father__isnull=True))