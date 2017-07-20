from .models import Host,Group
from rest_framework import serializers

class HostSerializer(serializers.ModelSerializer):
    group_id=serializers.CharField(source="group.id")
    class Meta:
        model=Host
        fields = ('id','name','group_id','sship','sshpasswd','sshport')
        depth = 1
    def create(self, validated_data):
        print(validated_data)
        group=Group.objects.get(id=validated_data['group']['id'])
        host=Host(
            name=validated_data['name'],
            group=group,
            sship=validated_data['sship'],
            sshpasswd=validated_data['sshpasswd'],
            sshport=validated_data['sshport'],
        )
        return host

class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ('id', 'name', 'remark')

