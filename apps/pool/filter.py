# -*- coding:utf-8 -*-
# !/usr/bin/env python
# Time 18-6-7
# Author Yo
# Email YoLoveLife@outlook.com
import django_filters
from pool import models
from django.db.models import Q

__all__ = [
    'IPFilter',
]


class IPFilter(django_filters.FilterSet):
    ip = django_filters.CharFilter(method="ip_filter")

    class Meta:
        model = models.IP_Pool
        fields = ['ip', ]

    @staticmethod
    def ip_filter(queryset, first_name, value):
        address_list = value.split('.')
        '''
        地址如何检索
        如果list大小为4 那么按照列表对应检索即可
        如果list大小为3 那么按照列表对应的ABC BCD来检索
        如果list大小为2 那么按照列表对应的 AB BC CD来检索
        如果list大小为1 那么都检索一下
        
        '''
        # Split ''
        address_list = [address for address in address_list if address!='']
        if len(address_list) == 4:
            return queryset.filter(
                A_address__icontains=address_list[0],
                B_address=address_list[1],
                C_address=address_list[2],
                D_address__icontains=address_list[3]
            )
        elif len(address_list) == 3:
            return queryset.filter(
                Q(
                    A_address__icontains=address_list[0],
                    B_address=address_list[1],
                    C_address__icontains=address_list[2]
                  )|Q(
                    B_address__icontains=address_list[0],
                    C_address=address_list[1],
                    D_address__icontains=address_list[2]
                )
            )
        elif len(address_list) == 2:
            return queryset.filter(
                Q(
                    A_address__icontains=address_list[0],
                    B_address__icontains=address_list[1]
                )|Q(
                    B_address__icontains=address_list[0],
                    C_address__icontains=address_list[1],
                )|Q(
                    C_address__icontains=address_list[0],
                    D_address__icontains=address_list[1],
                )
            )
        elif len(address_list) == 1:
            return queryset.filter(
                Q(
                    A_address__icontains=address_list[0],
                )|Q(
                    B_address__icontains=address_list[0],
                )|Q(
                    C_address__icontains=address_list[0],
                )|Q(
                    D_address__icontains=address_list[0]
                )
            )

