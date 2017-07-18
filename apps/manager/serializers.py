from .models import Host,Group
from rest_framework import serializers
from rest_framework.viewsets import ModelViewSet
from django.contrib.auth.models import User
class HostSerializer(serializers.ModelSerializer):
    class Meta:
        module=Host
        fields=('id','name','group','sship','sshpasswd','sshport')



class GroupSerializer(serializers.ModelSerializer):
    '''
    class Meta:
        module=Group
        fields=('id','name','remark')
    '''
    id=serializers.IntegerField(read_only=True)
    name=serializers.CharField(required=False,max_length=100,)
    remark=serializers.CharField(required=False,max_length=100,)
