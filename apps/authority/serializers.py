# -*- coding: utf-8 -*-
from rest_framework import serializers
from django.contrib.auth.models import Permission
from authority.models import ExtendUser,Group,Key,Jumper
from deveops.utils.rsa import ssh_keygen

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
    pub_key = serializers.CharField(max_length=4096, required=False, source='public_key')
    class Meta:
        model = Key
        fields = (
            'id', 'uuid', 'pub_key','name', 'group_name', 'fetch_time'
        )
        read_only_fields = (
            'id', 'uuid', 'pub_key','group_name', 'fetch_time'
        )

    def create(self, validated_data):
        pri,pub = ssh_keygen()
        validated_data['private_key'] = pri
        validated_data['public_key'] = pub
        return super(KeySerializer,self).create(validated_data)


class JumperSerializer(serializers.ModelSerializer):
    class Meta:
        model = Jumper
        fields = (
            'id', 'uuid', 'connect_ip', 'sshport', 'name', 'info', 'status'
        )
        read_only_fields = (
            'id', 'uuid', 'status'
        )
