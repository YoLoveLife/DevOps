import models
from manager.models import System_Type,Sys_User
from rest_framework import serializers

class JumperSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.Jumper
        fields = ('id', 'service_ip', 'normal_user','sshpasswd','sshport','info','status'
                )

class SystemTypeDetailSerializer(serializers.HyperlinkedModelSerializer):
    host_sum = serializers.StringRelatedField(source="sum_host",read_only=True)
    class Meta:
        model = System_Type
        fields = ("id","name","host_sum")

class SystemTypeSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = System_Type
        fields = ('id','name')

class SysUserSerializer(serializers.HyperlinkedModelSerializer):
    group_list = serializers.StringRelatedField(source="groups_list", read_only=True)
    is_admin = serializers.StringRelatedField(source='is_admin',read_only=True)
    reco_private_key = serializers.StringRelatedField(source='reco_private_key',read_only=True)
    class Meta:
        models = Sys_User
        fields = ('id','username','become_method','group_list','is_admin','reco_private_key')