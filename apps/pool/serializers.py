# -*- coding:utf-8 -*-
from pool import models
from rest_framework import serializers

__all__ = [
    "PoolSerializer",
]


class PoolSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.IP_Pool
        fields = (
            'id', 'ip_address', 'info', 'type',
        )
