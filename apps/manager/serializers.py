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


class HostUpdateStorageSerializer(serializers.ModelSerializer):
    storages=serializers.PrimaryKeyRelatedField(many=True,queryset=Storage.objects.all())
    class Meta:
        model = Host
        fields = ['id','storages']

    def create(self, validated_data):
        return

    def update(self, instance, validated_data):
        return