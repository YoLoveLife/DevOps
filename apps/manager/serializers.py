from .models import Host,Group,Storage
from rest_framework import serializers
class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ('id', 'name', 'info',
                )

class StorageSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Storage
        fields = ('id','disk_size','disk_path','info'
                  )

class HostSerializer(serializers.ModelSerializer):
    groups=GroupSerializer()
    class Meta:
        model=Host
        fields = ('id','groups','systemtype','manage_ip','service_ip','outer_ip','server_position','hostname',
                  'normal_user','sshpasswd','sshport','coreness','memory','root_disk','info'
                  ,'storages'
                  )


class HostUpdateStorageSerializer(serializers.ModelSerializer):
    storages=serializers.PrimaryKeyRelatedField(many=True,queryset=Storage.objects.all())
    class Meta:
        model = Host
        fields = ['id','storages']

    def create(self, validated_data):
        return

    def update(self, instance, validated_data):
        return


class HostUpdateGroupSerializer(serializers.ModelSerializer):
    hosts = serializers.PrimaryKeyRelatedField(many=True,queryset=Host.objects.all())
    class Meta:
        model = Group
        fields = ['id', 'hosts']