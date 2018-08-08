# -*- coding:utf-8 -*-
from rest_framework import serializers
from zdb import models
from manager.models import Group,Host
from zdb.tasks import instance_create
__all__ = [
    'ZDBInstanceGroupSerializer', "DBInstanceCreateSerializer",
    "DBInstanceImportSerializer", "ZDBInstanceSerializer",
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
    _status = serializers.IntegerField(required=False, source='status', )
    passwd = serializers.CharField(required=False, allow_null=True, source='password', write_only=True)

    _connect_ip = serializers.CharField(required=False, allow_null=True, source='connect_ip', )
    groupname = serializers.CharField(source="group_name", read_only=True)

    class Meta:
        model = models.Instance
        fields = (
            'id', 'uuid', 'name', '_connect_ip', 'port', 'aliyun_id', 'host', 'admin_user', '_status', 'passwd', 'type',
            'groupname'
        )
        read_only_fields = (
            'id', 'uuid', 'groupname'
        )


class DBInstanceImportSerializer(ZDBInstanceSerializer):
    class Meta:
        model = models.Instance
        fields = (
            'id', 'uuid', 'name', '_connect_ip', 'port', 'aliyun_id', 'host', 'admin_user', '_status', 'passwd', 'type', 'groupname'
        )
        read_only_fields = (
            'id', 'uuid', 'groupname'
        )

    def create(self, validated_data):
        return super(DBInstanceImportSerializer, self).create(validated_data)

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


class DBInstanceCreateSerializer(ZDBInstanceSerializer):
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
        obj = super(DBInstanceCreateSerializer, self).create(validated_data)
        instance_create.delay(obj, detail)
        return object