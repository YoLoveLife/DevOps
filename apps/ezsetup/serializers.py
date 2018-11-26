# -*- coding:utf-8 -*-
# !/usr/bin/env python
# Time 18-7-3
# Author Yo
# Email YoLoveLife@outlook.com
from rest_framework import serializers
from ezsetup import models
from manager.models import Group, Host
from ezsetup.tasks import install_redis

__all__ = [

]


class EZSetupSerializer(serializers.HyperlinkedModelSerializer):

    hosts = serializers.PrimaryKeyRelatedField(required=False,many=True, queryset=models.Host.objects.all(),
                                               allow_null=True)
    group = serializers.PrimaryKeyRelatedField(queryset=models.Group.objects.all())

    class Meta:
        model = models.SETUP
        fields = (
            'id', 'uuid', 'create_time', 'finish_time', 'type', 'group', 'hosts', 'status'
        )
        read_only_fields = (
            'id', 'uuid',
        )


class DetailRedisSerializer(serializers.Serializer):
    redis_port = serializers.IntegerField()
    version = serializers.CharField()
    redis_passwd = serializers.CharField()

    class Meta:
        fields = (
            'redis_port', 'redis_passwd', 'version'
        )


class EZSetupRedisSerializer(EZSetupSerializer):
    detail = DetailRedisSerializer(write_only=True)

    class Meta:
        model = models.SETUP
        fields = (
            'id', 'uuid', 'create_time', 'finish_time', 'type', 'group', 'hosts', 'detail'
        )
        read_only_fields = (
            'id', 'uuid',
        )

    def create(self, validated_data):
        detail = validated_data.pop('detail')
        obj = super(EZSetupRedisSerializer, self).create(validated_data)
        install_redis.delay(obj, detail)
        return obj