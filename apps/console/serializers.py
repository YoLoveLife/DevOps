# -*- coding: utf-8 -*-
from console import models
from django.conf import settings
from rest_framework import serializers

__all__ = [

]


class ConsoleTruckSerializer(serializers.HyperlinkedModelSerializer):
    group = serializers.PrimaryKeyRelatedField(queryset=models.Group.objects.all(), write_only=True)

    class Meta:
        model = models.Truck
        fields = (
            'id', 'uuid', 'group'
        )
        read_only_fields = (
            'id', 'uuid',
        )
        write_only_fields = (
            'group'
        )

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super(ConsoleTruckSerializer, self).create(validated_data)
