import models
from rest_framework import serializers

class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.Group
        fields = ('id', 'name', 'info',
                )

class StorageSerializer(serializers.HyperlinkedModelSerializer):
    group_name = serializers.StringRelatedField(source="get_all_group_name",read_only=True)
    class Meta:
        model = models.Storage
        fields = ('id','disk_size','disk_path','info','group_name',
                  )

class HostSerializer(serializers.ModelSerializer):
    systemtype = serializers.CharField(source='systemtype.name')
    class Meta:
        model=models.Host
        fields = ('id','systemtype','manage_ip','service_ip','outer_ip','server_position','hostname',
                  'normal_user','sshport','coreness','memory','root_disk','info'
                  ,'storages','status',
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