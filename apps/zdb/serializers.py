# -*- coding:utf-8 -*-
from rest_framework import serializers
from zdb import models
from manager.models import Group,Host
__all__ = [
    'DBInstanceGroupSerializer'
]


class DBInstanceGroupSerializer(serializers.HyperlinkedModelSerializer):
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


class DBInstanceSerializer(serializers.HyperlinkedModelSerializer):

    host = serializers.PrimaryKeyRelatedField(required=False, allow_null=True,
                                                   queryset=models.Host.objects.all())
    _status = serializers.IntegerField(required=False, source='status',)
    passwd = serializers.CharField(required=False, allow_null=True, source='password', write_only=True)

    groupname = serializers.CharField(source="group_name", read_only=True)
    class Meta:
        model = models.Instance
        fields = (
            'id', 'uuid', 'name', 'connect_ip', 'port', 'aliyun_id', 'host', 'admin_user', '_status', 'passwd', 'type', 'groupname'
        )
        read_only_fields = (
            'id', 'uuid', 'groupname'
        )
