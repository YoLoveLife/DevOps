# -*- coding:utf-8 -*-
from timeline import models
from rest_framework import serializers

__all__ = [
    "HistorySerializer",
]

class HistorySerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = models.History
        fields = (
            'id', 'uuid', 'msg', 'type', 'time',
        )
        read_only_fields = (
            'id', 'uuid',
        )
