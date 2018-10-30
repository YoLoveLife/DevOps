# -*- coding:utf-8 -*-
from rest_framework import serializers
from zdb import models
from manager.models import Group,Host
from zdb.tasks import instance_create
from zdb.tasks import status_flush
__all__ = [
    'ZDBInstanceGroupSerializer', "ZDBInstanceCreateSerializer",
    "ZDBInstanceImportSerializer", "ZDBInstanceSerializer",
]


class ZDBInstanceGroupSerializer(serializers.HyperlinkedModelSerializer):
    group = serializers.PrimaryKeyRelatedField(required=True, queryset=Group.objects.all(),allow_null=True)
    instances = serializers.PrimaryKeyRelatedField(required=False, many=True, allow_null=True, queryset=models.Instance.objects.all())

    groupname = serializers.CharField(source="group_name", read_only=True)
    _status = serializers.IntegerField(required=False, source='status', read_only=True)

    instancecount = serializers.IntegerField(source="instance_count", read_only=True)
    databasecount = serializers.IntegerField(source="database_count", read_only=True)

    class Meta:
        model = models.InstanceGroup
        fields = (
            'id', 'uuid', 'group', 'instances', 'name', 'groupname', '_status', 'instancecount', 'databasecount'
        )
        read_only_fields = (
            'id', 'uuid', 'instancecount', 'databasecount', '_status'
        )

class ZDBInstanceSerializer(serializers.HyperlinkedModelSerializer):
    host = serializers.PrimaryKeyRelatedField(required=False, allow_null=True,
                                              queryset=models.Host.objects.all())
    passwd = serializers.CharField(required=False, allow_null=True, source='password', write_only=True)

    _connect_ip = serializers.CharField(required=False, allow_null=True, source='connect_ip', )
    group = serializers.PrimaryKeyRelatedField(required=True, allow_null=False, queryset=models.InstanceGroup.objects.all())

    groupname = serializers.CharField(source="group_name", read_only=True)

    class Meta:
        model = models.Instance
        fields = (
            'id', 'uuid', 'name', '_connect_ip', 'port', 'aliyun_id', 'host', 'admin_user', 'status', 'passwd', 'type', 'group',
            'groupname'
        )
        read_only_fields = (
            'id', 'uuid', 'groupname', 'status'
        )


class ZDBInstanceImportSerializer(ZDBInstanceSerializer):
    class Meta:
        model = models.Instance
        fields = (
            'id', 'uuid', 'name', '_connect_ip', 'port', 'aliyun_id', 'host', 'admin_user', 'status', 'passwd', 'type', 'groupname',
            'group'
        )
        read_only_fields = (
            'id', 'uuid', 'groupname', 'status'
        )

    def create(self, validated_data):
        obj = super(ZDBInstanceImportSerializer, self).create(validated_data)
        status_flush.delay(obj)
        return obj


class DetailSerializer(serializers.Serializer):
    memory = serializers.IntegerField()
    port = serializers.IntegerField()
    version = serializers.CharField()
    group = serializers.PrimaryKeyRelatedField(required=False, allow_null=True,
                                              queryset=models.Group.objects.all())

    class Meta:
        fields = (
            'memory', 'port', 'version', 'group'
        )


class ZDBInstanceCreateSerializer(ZDBInstanceSerializer):
    detail = DetailSerializer(write_only=True)
    class Meta:
        model = models.Instance
        fields = (
            'id', 'uuid', 'name', '_connect_ip', 'port', 'aliyun_id',
            'host', 'admin_user', '_status', 'passwd', 'type', 'groupname', 'detail',
        )
        read_only_fields = (
            'id', 'uuid', 'groupname'
        )

    def create(self, validated_data):
        detail = validated_data.pop('detail')
        obj = super(ZDBInstanceCreateSerializer, self).create(validated_data)
        instance_create.delay(obj, detail)
        return object