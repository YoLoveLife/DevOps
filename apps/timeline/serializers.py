# -*- coding:utf-8 -*-
from manager import models
from rest_framework import serializers
from authority.models import ExtendUser

__all__ = [
    "HistorySerializer",
]


class HistorySerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = models.History
        fields = (
            'id', 'uuid', 'name', 'info', '_status', 'users', '_framework', 'pmn_groups', 'key', 'jumper', 'framework',
        )
        read_only_fields = (
            'id', 'uuid', 'framework'
        )
        write_only_fields = (
            '_framework'
        )

