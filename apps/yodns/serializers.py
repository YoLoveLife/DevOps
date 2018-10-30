# -*- coding:utf-8 -*-
from yodns import models
from rest_framework import serializers

__all__ = [
    "DNSSerializer"
]

class DNSSerializer(serializers.HyperlinkedModelSerializer):
    group_name = serializers.CharField(source='group.name', read_only=True)
    group = serializers.PrimaryKeyRelatedField(required=False, queryset=models.Group.objects.all(),allow_null=True)


    class Meta:
        model = models.DNS
        fields = (
            'id', 'uuid', 'group_name', 'group', 'internal_dig', 'external_dig', 'url'
        )
        read_only_fields = (
            'id', 'uuid', 'group_name',
        )