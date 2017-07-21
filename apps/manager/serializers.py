from .models import Host,Group
from rest_framework import serializers

class HostSerializer(serializers.ModelSerializer):
    #group_id=serializers.CharField(source="group.id")
    #group=GroupSerializer()
    class Meta:
        model=Host
        fields = ('id','name',
                  #'group_id',
     #             'group',
                  'sship','sshpasswd','sshport')



class GroupSerializer(serializers.HyperlinkedModelSerializer):
    host_set=HostSerializer(many=True,read_only=True)
    class Meta:
        model = Group
        fields = ('id', 'name', 'remark',
                  'host_set',
                )




