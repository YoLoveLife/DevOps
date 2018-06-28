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
    groupname = serializers.CharField(source="group_name", read_only=True)

    class Meta:
        model = models.Instance
        fields = (
            'id', 'uuid', 'group', 'name', 'port', 'is_master', 'admin_user', 'passwd', '_status', 'hosts', 'groupname'
        )
        read_only_fields = (
            'id', 'uuid', 'groupname'
        )


class DBRoleSerializer(serializers.HyperlinkedModelSerializer):
    instance = serializers.PrimaryKeyRelatedField(required=True, queryset=models.Instance.objects.all(),allow_null=True)
    instance_name = serializers.CharField(source="instance.name", read_only=True)
    permissions = serializers.ListField(source='permission_list', allow_null=True)
    groupname = serializers.CharField(source="group_name", read_only=True)
    class Meta:
        model = models.Role
        fields = (
            'id', 'uuid', 'name', 'permissions', 'groupname', 'instance_name', 'instance', 'info'
        )
        read_only_fields = (
            'id', 'uuid', 'group', 'instance_name'
        )


class DBUserSerializer(serializers.HyperlinkedModelSerializer):
    roleinfo = serializers.CharField(source="role_info")
    role = serializers.PrimaryKeyRelatedField(required=True, queryset=models.Instance.objects.all(),allow_null=True)
    groupname = serializers.CharField(source="group_name", read_only=True)
    passwd = serializers.CharField(required=False, allow_null=True, source='password',write_only=True)
    _status = serializers.IntegerField(required=True, source='status',)
    class Meta:
        model = models.User
        fields = (
            'id', 'uuid', 'username', 'role', 'passwd', '_status', 'info', 'roleinfo', 'groupname'
        )