# -*- coding: utf-8 -*-
from rest_framework import serializers
from django.contrib.auth.models import Permission
from authority.models import ExtendUser,Group,Key,Jumper

__all__ = [
    'UserSerializer', 'GroupSerializer', 'PermissionSerializer',
    'KeySerializer'
]

class UserSerializer(serializers.ModelSerializer):
    group_name = serializers.StringRelatedField(source="get_group_name", read_only=True)
    email8531 = serializers.StringRelatedField(source="get_8531email", read_only=True)
    groups = serializers.PrimaryKeyRelatedField(many=True, queryset=Group.objects.all())

    class Meta:
        model = ExtendUser
        fields = (
            'id', 'is_active', 'last_login', 'phone', 'username', 'full_name', 'group_name', 'email8531', 'groups'
        )


class GroupSerializer(serializers.ModelSerializer):
    permissions = serializers.PrimaryKeyRelatedField(many=True,queryset=Permission.objects.all())

    class Meta:
        model = Group
        fields = (
            'id', 'name', 'permissions'
        )


class PermissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Permission
        fields = (
            'id', 'name'
        )


class KeySerializer(serializers.ModelSerializer):
    private_key = serializers.CharField(max_length=4096, required=False)
    public_key = serializers.CharField(max_length=4096, required=False)

    class Meta:
        model = Key
        fields = (
            'id', 'name', 'private_key', 'public_key', 'group_name', 'fetch_time'
        )
        read_only_fields = (
            'id', 'group_name', 'fetch_time'
        )


class JumperSerializer(serializers.ModelSerializer):
    class Meta:
        model = Jumper
        fields = (
            'id', 'connect_ip', 'sshport', 'name', 'info', 'status'
        )
        read_only_fields = (
            'id', 'status'
        )
