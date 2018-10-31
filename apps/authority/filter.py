# -*- coding:utf-8 -*-
# !/usr/bin/env python
# Time 18-6-7
# Author Yo
# Email YoLoveLife@outlook.com
from django.contrib.auth.models import Permission,Group
from django.db.models import Q
import django_filters
from manager import models

__all__ = [
    'UserFilter', 'GroupFilter', 'KeyFilter', 'JumperFilter'
]


class UserFilter(django_filters.FilterSet):
    phone = django_filters.CharFilter(method="phone_filter")
    name = django_filters.CharFilter(method="name_filter")
    username = django_filters.CharFilter(method="username_filter")
    is_active = django_filters.CharFilter(method="is_active_filter")

    class Meta:
        model = models.ExtendUser
        fields = ['phone', 'name', 'username', 'email', 'is_active']

    @staticmethod
    def phone_filter(queryset, first_name, value):
        return queryset.filter(phone__icontains=value)

    @staticmethod
    def name_filter(queryset, first_name, value):
        return queryset.filter(Q(first_name__icontains=value)|Q(full_name__icontains=value))

    @staticmethod
    def username_filter(queryset, first_name, value):
        return queryset.filter(username__icontains=value)

    @staticmethod
    def is_active_filter(queryset, first_name, value):
        return queryset.filter(is_active=value)


class GroupFilter(django_filters.FilterSet):
    permission = django_filters.CharFilter(method="permission_filter")
    name = django_filters.CharFilter(method="name_filter")

    class Meta:
        model = Group
        fields = ['permission', 'name']

    @staticmethod
    def permission_filter(queryset, first_name, value):
        ps = Permission.objects.filter(codename__icontains="yo_").filter(name__icontains=value)
        return queryset.filter(permissions__in=ps).distinct()

    @staticmethod
    def name_filter(queryset, first_name, value):
        return queryset.filter(name__icontains=value)


class KeyFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(method="name_filter")
    group_name = django_filters.CharFilter(method="group_name_filter")

    class Meta:
        model = models.Key
        fields = ['name', ]

    @staticmethod
    def name_filter(queryset, first_name, value):
        return queryset.filter(name__icontains=value)

    @staticmethod
    def group_name_filter(queryset, first_name, value):
        groups = models.Group.objects.filter(name__icontains=value)
        return queryset.filter(group__in=groups)


class JumperFilter(django_filters.FilterSet):
    info = django_filters.CharFilter(method="info_filter")
    group_name = django_filters.CharFilter(method="group_name_filter")

    class Meta:
        model = models.Jumper
        fields = ['info', 'group_name']

    @staticmethod
    def info_filter(queryset, first_name, value):
        return queryset.filter(Q(name__icontains=value)|Q(info__icontains=value))

    @staticmethod
    def group_name_filter(queryset, first_name, value):
        groups = models.Group.objects.filter(name__icontains=value)
        return queryset.filter(group__in=groups)
