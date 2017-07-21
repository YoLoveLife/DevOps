from .models import Host,Group
from rest_framework import serializers

class HostSerializer(serializers.ModelSerializer):
    #group_id=serializers.CharField(source="group.id")
    #group=GroupSerializer()
    class Meta:
        model=Host
        fields = ('id','systemtype','manage_ip','service_ip','outer_ip','server_position','hostname',
                  'normal_user','sshpasswd','sshport','coreness','memory','root_disk','share_disk','share_disk_path','info')

class GroupSerializer(serializers.HyperlinkedModelSerializer):
    host_set=HostSerializer(many=True,read_only=True)
    class Meta:
        model = Group
        fields = ('id', 'name', 'info',
                  'host_set',
                )




