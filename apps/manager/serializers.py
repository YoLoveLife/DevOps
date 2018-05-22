# -*- coding:utf-8 -*-
from manager import models
from rest_framework import serializers
from authority.models import ExtendUser

__all__ = [
    "GroupSerializer", "SystemTypeSerializer", 'PositionSerializer',
    "HostDetailSerializer", "HostSerializer", "HostPasswordSerializer",
    "StorageSerializer"
]


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    users = serializers.PrimaryKeyRelatedField(many=True, queryset=ExtendUser.objects.all())
    pmn_groups = serializers.PrimaryKeyRelatedField(many=True, queryset=models.PerGroup.objects.all())
    key = serializers.PrimaryKeyRelatedField(required=False, queryset=models.Key.objects.all(), allow_null=True)
    jumper = serializers.PrimaryKeyRelatedField(required=False, queryset=models.Jumper.objects.all(), allow_null=True)
    _status = serializers.IntegerField(required=True, source='status',)
    _framework = serializers.PrimaryKeyRelatedField(queryset=models.FILE.objects.all(), allow_null=True)
    framework = serializers.ImageField(source="_framework.image", read_only=True)
    class Meta:
        model = models.Group
        fields = (
            'id', 'uuid', 'name', 'info', '_status', 'users', '_framework', 'pmn_groups', 'key', 'jumper', 'framework',
        )
        read_only_fields = (
            'id', 'uuid', 'framework'
        )

    def update(self, instance, validated_data):
        # instance.framework_update()
        # 刪除原有的外鍵以及相關的文件
        return super(GroupSerializer,self).update(instance,validated_data)

class GroupSelectHostSerializer(GroupSerializer):
    hosts = serializers.PrimaryKeyRelatedField(queryset=models.Host.objects.all(), many=True)
    class Meta:
        model = models.Group
        fields = (
            'id', 'hosts'
        )
    def update(self, instance, validated_data):
        # instance.framework_update()
        # 刪除原有的外鍵以及相關的文件
        print('123')
        return super(GroupSerializer,self).update(instance,validated_data)

# class GroupSelectHostSerializer(serializers.Serializer):
#     hosts = serializers.ListField()
#     class Meta:
#         model = models.Group
#         # fields = (
#         #     'id', 'hosts'
#         # )
#
#     def update(self, instance, validated_data):
#         hosts = validated_data.pop('hosts')
#         print(validated_data)
#         id_list = []
#         for host in hosts:
#             id_list.append(host['id'])
#         hosts = models.Host.objects.filter(id__in=id_list)
#
#         for host in hosts:
#             print(type(host))
#             instance.hosts.add(host)
#         instance.save()
#
#         return super(GroupSelectHostSerializer,self).update(instance,validated_data)


class SystemTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.System_Type
        fields = (
            'id', 'name'
        )


class PositionSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Position
        fields = (
            'id', 'name'
        )


class HostDetailSerializer(serializers.ModelSerializer):
    systemtype = serializers.PrimaryKeyRelatedField(queryset=models.System_Type.objects.all())
    position = serializers.PrimaryKeyRelatedField(queryset=models.Position.objects.all())

    class Meta:
        model = models.HostDetail
        fields = (
            'position', 'systemtype', 'info', 'aliyun_id', 'vmware_id'
        )


class HostSerializer(serializers.ModelSerializer):
    detail = HostDetailSerializer(required=True)
    groups = serializers.PrimaryKeyRelatedField(many=True, required=False, allow_null=True, queryset=models.Group.objects.all())
    passwd = serializers.CharField(required=False, allow_null=True, source='password',)
    _status = serializers.IntegerField(required=True, source='status',)

    class Meta:
        model = models.Host
        fields = (
            'id', 'detail', 'connect_ip', 'service_ip', 'hostname', 'sshport', '_status', 'groups',
            'passwd', 'uuid'
        )
        read_only_fields = (
            'id', 'uuid'
        )

    def create(self, validated_data):
        detail = validated_data.pop('detail')
        detail_instance = models.HostDetail.objects.create(**detail)
        validated_data.pop('groups')
        return models.Host.objects.create(detail=detail_instance, **validated_data)

    def update(self, instance, validated_data):
        detail = validated_data.pop('detail')
        for v in detail:
            if hasattr(instance.detail,v):
                setattr(instance.detail,v,detail.get(v))
        instance.detail.save()
        return super(HostSerializer,self).update(instance,validated_data)


class HostPasswordSerializer(serializers.ModelSerializer):
    passwd = serializers.CharField(required=True, source='password')

    class Meta:
        model = models.Host
        fields = (
            'id', 'passwd',
        )
        read_only_fields = (
            'id', 'passwd',
        )


class StorageSerializer(serializers.HyperlinkedModelSerializer):
    group_name = serializers.StringRelatedField(source="get_all_group_name",read_only=True)

    class Meta:
        model = models.Storage
        fields = (
            'id', 'disk_size', 'disk_path', 'info', 'group_name'
        )
