import models
from rest_framework import serializers
from authority.models import ExtendUser

__all__ = [
    "GroupSerializer", "SystemTypeSerializer", 'PositionSerializer',
    "HostDetailSerializer", "HostSerializer", "HostPasswordSerializer",
    "StorageSerializer"
]


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    users = serializers.PrimaryKeyRelatedField(many=True,queryset=ExtendUser.objects.all())
    pmn_groups = serializers.PrimaryKeyRelatedField(many=True,queryset=models.PerGroup.objects.all())

    class Meta:
        model = models.Group
        fields = (
            'id', 'name', 'info', 'uuid', 'status', 'users', 'framework', 'pmn_groups',
        )
        read_only_fields = (
            'id', 'framework'
        )


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
    label = serializers.CharField(source='__unicode__',read_only=True)
    detail = HostDetailSerializer(required=True)
    groups = serializers.PrimaryKeyRelatedField(many=True, required=False, allow_null=True, queryset=models.Group.objects.all())
    passwd = serializers.CharField(required=False, allow_null=True, source='password',)

    class Meta:
        model = models.Host
        fields = (
            'id', 'label', 'detail', 'connect_ip', 'service_ip', 'hostname', 'sshport', 'status', 'groups',
            'passwd',
        )
        read_only_fields = (
            'id', 'label'
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