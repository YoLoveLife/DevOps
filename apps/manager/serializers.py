import models
from rest_framework import serializers
from authority.models import ExtendUser

class GroupSerializer(serializers.HyperlinkedModelSerializer):
    users = serializers.PrimaryKeyRelatedField(many=True,queryset=ExtendUser.objects.all())
    class Meta:
        model = models.Group
        fields = ('id', 'name', 'info', 'uuid', 'status','users',#'framework'
                )
        read_only_fields = ('id',
                             )

class StorageSerializer(serializers.HyperlinkedModelSerializer):
    group_name = serializers.StringRelatedField(source="get_all_group_name",read_only=True)
    class Meta:
        model = models.Storage
        fields = ('id','disk_size','disk_path','info','group_name',
                  )

class SystemTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.System_Type
        fields = (
            'name',
        )

class HostDetailSerializer(serializers.ModelSerializer):
    systemtype=SystemTypeSerializer()
    class Meta:
        model = models.HostDetail
        fields = (
            'coreness','memory','root_disk','server_position','systemtype','info',
        )

class HostSerializer(serializers.ModelSerializer):
    label = serializers.CharField(source='__unicode__')
    detail = HostDetailSerializer()
    class Meta:
        model=models.Host
        fields = (
            'id','uuid','label','detail',
        )


class HostPasswordSerializer(serializers.ModelSerializer):
    password = serializers.StringRelatedField(source='password_get',read_only=True)
    class Meta:
        model=models.Host
        fields = ('id','password')


class HostUpdateGroupSerializer(serializers.ModelSerializer):
    hosts = serializers.PrimaryKeyRelatedField(many=True,queryset=models.Host.objects.all())
    class Meta:
        model = models.Group
        fields = ['id', 'hosts']

class HostSearchSerializer(serializers.ModelSerializer):
    groups__name = serializers.CharField()
    storages__disk_size = serializers.CharField()
    storages__disk_path = serializers.CharField()
    class Meta:
        model=models.Host
        fields = ('manage_ip','service_ip','outer_ip','server_position','hostname','groups__name',
                  'normal_user','sshpasswd','sshport','coreness','memory','root_disk','info'
                  ,'storages__disk_size','storages__disk_path'
                  )