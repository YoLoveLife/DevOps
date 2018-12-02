# -*- coding: utf-8 -*-
from variable import models
from rest_framework import serializers

__all__ = [
    'Var2GroupSerializer',
]


class Var2GroupSerializer(serializers.ModelSerializer):
    group = serializers.PrimaryKeyRelatedField(required=False, queryset=models.Group.objects.all(), allow_null=True)

    class Meta:
        model = models.Var2Group
        fields = (
            'id', 'key', 'value', 'group', 'uuid'
        )
        read_only_fields = (
            'id', 'uuid'
        )