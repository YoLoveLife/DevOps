# -*- coding:utf-8 -*-
# !/usr/bin/env python
# Time 18-6-7
# Author Yo
# Email YoLoveLife@outlook.com
import django_filters
from db import models
from manager.models import Group
from django.db.models import Q

__all__ = [
    'DBInstanceFilter', 'DBRoleFilter',
]


class DBInstanceFilter(django_filters.FilterSet):
    is_master = django_filters.CharFilter(method="is_master_filter")
    group = django_filters.CharFilter(method="group_filter")
    name = django_filters.CharFilter(method="name_filter")
    status = django_filters.CharFilter(method="status_filter")

    class Meta:
        model = models.Instance
        fields = ['is_master', 'group', 'name', 'status']

    @staticmethod
    def is_master_filter(queryset, first_name, value):
        print('kkkkkk',value)
        return queryset.filter(is_master=value)

    @staticmethod
    def group_filter(queryset, first_name, value):
        group = Group.objects.filter(id=value)
        return queryset.filter(group__in=group)

    @staticmethod
    def name_filter(queryset, first_name, value):
        return queryset.filter(name__icontains=value)

    @staticmethod
    def status_filter(queryset, first_name, value):
        return queryset.filter(_status=value)


class DBRoleFilter(django_filters.FilterSet):
    group = django_filters.CharFilter(method="group_filter")
    name = django_filters.CharFilter(method="name_filter")
    update = django_filters.CharFilter(method="update_filter")
    delete = django_filters.CharFilter(method="delete_filter")
    drop = django_filters.CharFilter(method="drop_filter")
    class Meta:
        model = models.Role
        fields = ['group', 'update', 'delete', 'drop']

    @staticmethod
    def group_filter(queryset, first_name, value):
        groups = Group.objects.filter(name=value)
        instances = models.Instance.objects.filter(group__in=groups)
        return queryset.filter(instance__in=instances)

    @staticmethod
    def name_filter(queryset, first_name, value):
        return queryset.filter(name__icontains=value)

    @staticmethod
    def update_filter(queryset, first_name, value):
        return queryset.filter(update=value)

    @staticmethod
    def delete_filter(queryset, first_name, value):
        return queryset.filter(delete=value)

    @staticmethod
    def drop_filter(queryset, first_name, value):
        return queryset.filter(drop=value)