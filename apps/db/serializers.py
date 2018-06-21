# -*- coding:utf-8 -*-
from rest_framework import serializers
from db import models
from manager.models import Group,Host
__all__ = [
    'DBInstanceSerializer', 'DBRoleSerializer'
]


class DBInstanceSerializer(serializers.HyperlinkedModelSerializer):
    group = serializers.PrimaryKeyRelatedField(required=True, queryset=Group.objects.all(),allow_null=True)
    hosts = serializers.PrimaryKeyRelatedField(many=True, required=False, allow_null=True, queryset=Host.objects.all())
    is_master = serializers.BooleanField(required=True)
    passwd = serializers.CharField(required=False, allow_null=True, source='_admin_passwd',)
    _status = serializers.IntegerField(required=True, source='status',)

    class Meta:
        model = models.Instance
        fields = (
            'id', 'uuid', 'group', 'name', 'port', 'is_master', 'admin_user', 'passwd', '_status', 'hosts',
        )
        read_only_fields = (
            'id', 'uuid',
        )


class DBRoleSerializer(serializers.HyperlinkedModelSerializer):
    instance = serializers.PrimaryKeyRelatedField(required=True, queryset=models.Instance.objects.all(),allow_null=True)
    permissions = serializers.ListField(source='permission_list')
    group = serializers.CharField(source="group_name")
    class Meta:
        model = models.Role
        fields = (
            'id', 'uuid', 'name', 'select', 'update', 'delete', 'insert', 'create', 'drop', 'alter', 'permissions', 'group', 'instance'
        )
        read_only_fields = (
            'id', 'uuid', 'permissions', 'group'
        )