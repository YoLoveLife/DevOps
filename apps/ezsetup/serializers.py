# -*- coding:utf-8 -*-
from rest_framework import serializers
from ezsetup import models
from manager.models import Group,Host
from ezsetup.tasks import install_redis,install_mysql
__all__ = [

]

class EZSetupSerializer(serializers.HyperlinkedModelSerializer):

    create_time = serializers.DateTimeField(source='push_mission.create_time', format="%Y-%m-%dT%H:%M:%S", read_only=True)
    finish_time = serializers.DateTimeField(source='push_mission.finish_time', format="%Y-%m-%dT%H:%M:%S", read_only=True)

    hosts = serializers.PrimaryKeyRelatedField(required=False,many=True, queryset=models.Host.objects.all(),allow_null=True)
    group = serializers.PrimaryKeyRelatedField(queryset=models.Group.objects.all())

    class Meta:
        model = models.SETUP
        fields = (
            'id', 'uuid', 'create_time', 'finish_time', 'type', 'group', 'hosts'
        )
        read_only_fields = (
            'id', 'uuid',
        )


class DetailMySQLSerializer(serializers.Serializer):
    memory = serializers.IntegerField()
    port = serializers.IntegerField()
    version = serializers.CharField()

    class Meta:
        fields = (
            'memory', 'port', 'version',
        )


class EZSetupMySQLSerializer(EZSetupSerializer):
    detail = DetailMySQLSerializer(write_only=True)
    class Meta:
        model = models.SETUP
        fields = (
            'id', 'uuid', 'create_time', 'finish_time', 'type', 'group', 'hosts', 'detail'
        )
        read_only_fields = (
            'id', 'uuid',
        )

    def create(self, validated_data):
        install_mysql.delay(None,validated_data)


class DetailRedisSerializer(serializers.Serializer):
    class Meta:
        fields = (

        )

class EZSetupRedisSerializer(EZSetupSerializer):
    # detail = DetailRedisSerializer(write_only=True)
    class Meta:
        model = models.SETUP
        fields = (
            'id', 'uuid', 'create_time', 'finish_time', 'type', 'group', 'hosts',# 'detail'
        )
        read_only_fields = (
            'id', 'uuid',
        )

    def create(self, validated_data):
        obj = super(EZSetupRedisSerializer, self).create(validated_data)
        install_redis.delay(obj, validated_data)
        return obj