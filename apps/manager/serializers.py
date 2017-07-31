from .models import Host,Group,Storage
from rest_framework import serializers
class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ('id', 'name', 'info',
                )

class StorageSerializer(serializers.HyperlinkedModelSerializer):
    group=GroupSerializer()
    class Meta:
        model = Storage
        fields = ('id','disk_size','disk_path','info'
                  ,'group'
                  )

class HostSerializer(serializers.ModelSerializer):
    group=GroupSerializer()
    class Meta:
        model=Host
        fields = ('id','group','systemtype','manage_ip','service_ip','outer_ip','server_position','hostname',
                  'normal_user','sshpasswd','sshport','coreness','memory','root_disk','info'
                  ,'storages','group'
                  )


