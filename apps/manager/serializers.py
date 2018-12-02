# -*- coding:utf-8 -*-
# !/usr/bin/env python
# Time 17-10-25
# Author Yo
# Email YoLoveLife@outlook.com
from rest_framework import serializers
from manager import models
from authority.models import ExtendUser

__all__ = [
    "GroupSerializer", "HostSerializer", "HostPasswordSerializer",
    'GroupSampleSerializer', 'HostSampleSerializer', 'GroupSelectHostSerializer', 'HostSelectGroupSerializer'
]


class GroupSampleSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.Group
        fields = (
            'id', 'uuid', 'name'
        )


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    users = serializers.PrimaryKeyRelatedField(required=False, many=True, queryset=ExtendUser.objects.all())
    pmn_groups = serializers.PrimaryKeyRelatedField(required=False, many=True, queryset=models.PerGroup.objects.all())
    key = serializers.PrimaryKeyRelatedField(required=False, queryset=models.Key.objects.all(), allow_null=True)
    jumper = serializers.PrimaryKeyRelatedField(required=False, queryset=models.Jumper.objects.all(), allow_null=True)
    _status = serializers.IntegerField(required=True, source='status',)
    _framework = serializers.PrimaryKeyRelatedField(required=False, queryset=models.IMAGE.objects.all(),
                                                    allow_null=True, write_only=True)
    framework = serializers.ImageField(source="_framework.image", read_only=True)

    class Meta:
        model = models.Group
        fields = (
            'id', 'uuid', 'name', 'info', '_status', 'users', '_framework', 'pmn_groups', 'key',
            'jumper', 'framework',
        )
        read_only_fields = (
            'id', 'uuid', 'framework'
        )
        write_only_fields = (
            '_framework'
        )

    def update(self, instance, validated_data):
        # instance.framework_update()
        # 刪除原有的外鍵以及相關的文件
        return super(GroupSerializer, self).update(instance,validated_data)


class GroupSelectHostSerializer(GroupSerializer):
    hosts = serializers.PrimaryKeyRelatedField(required=True, queryset=models.Host.objects.all(), many=True)

    class Meta:
        model = models.Group
        fields = (
            'id', 'hosts'
        )

    def update(self, instance, validated_data):
        # instance.hosts.add(validated_data['hosts'])
        instance.hosts.add(*validated_data['hosts'])
        validated_data.pop('hosts')
        return super(GroupSelectHostSerializer, self).update(instance, validated_data)
        # print(validated_data)
        # return super(GroupSelectHostSerializer,self).update(instance,validated_data)


class HostSampleSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Host
        fields = (
            'id', 'uuid', 'hostname'
        )


class HostSerializer(serializers.ModelSerializer):
    passwd = serializers.CharField(required=False, allow_null=True, source='password', write_only=True)
    _status = serializers.IntegerField(required=True, source='status',)
    groups = serializers.PrimaryKeyRelatedField(read_only=True, many=True,)

    class Meta:
        model = models.Host
        fields = (
            'id', 'connect_ip', 'hostname', 'sshport', '_status', 'groups',
            'passwd', 'uuid', 'position', 'systemtype', 'info', 'aliyun_id', 'vmware_id'
        )
        read_only_fields = (
            'id', 'uuid', 'groups'
        )
        write_only_fields = (
            'passwd',
        )


class HostPasswordSerializer(serializers.ModelSerializer):
    passwd = serializers.CharField(source='password', read_only=True)

    class Meta:
        model = models.Host
        fields = (
            'id', 'passwd',
        )
        read_only_fields = (
            'id', 'passwd',
        )


class HostSelectGroupSerializer(GroupSerializer):
    groups = serializers.PrimaryKeyRelatedField(many=True, queryset=models.Group.objects.all())

    class Meta:
        model = models.Host
        fields = (
            'id', 'groups'
        )
