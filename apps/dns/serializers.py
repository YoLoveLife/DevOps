# -*- coding:utf-8 -*-
from dns import models
from rest_framework import serializers

__all__ = [
    "DNSSerializer"
]


class DNSSerializer(serializers.HyperlinkedModelSerializer):
    group_name = serializers.CharField(source='group.name', read_only=True)
    father = serializers.PrimaryKeyRelatedField(required=False, queryset=models.DNS.objects.all(),allow_null=True)
    group = serializers.PrimaryKeyRelatedField(required=False, queryset=models.Group.objects.all(),allow_null=True)
    dns_name = serializers.CharField(source='__unicode__', read_only=True)
    _level = serializers.IntegerField(source='level', read_only=True)

    class Meta:
        model = models.DNS
        fields = (
            'id', 'uuid', 'group_name', 'name', 'dig', 'inner_dig', 'father', 'group', 'dns_name', '_level'
        )
        read_only_fields = (
            'id', 'uuid', 'group_name', 'dns_name', '_level'
        )