from .models import Host,Group,Storage
from rest_framework import serializers

class StorageSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Storage
        fields = ('id','disk_size','disk_path','info')

class HostSerializer(serializers.ModelSerializer):
    storages=StorageSerializer(many=True,read_only=True)
    class Meta:
        model=Host
        fields = ('id','group','systemtype','manage_ip','service_ip','outer_ip','server_position','hostname',
                  'normal_user','sshpasswd','sshport','coreness','memory','root_disk','share_disk','share_disk_path','info','storages')

class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ('id', 'name', 'info',
                )



