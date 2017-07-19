from .models import Host,Group
from rest_framework import serializers
from rest_framework.viewsets import ModelViewSet
from django.contrib.auth.models import User

class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ('id','name','remark')

class HostSerializer(serializers.HyperlinkedModelSerializer):
    group_id=serializers.CharField(source="group.id")
    class Meta:
        model=Host
        fields = ('id','name','group_id','sship','sshpasswd','sshport')
        depth = 1



