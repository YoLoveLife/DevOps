import models
from manager.models import System_Type
from rest_framework import serializers

class JumperSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.Jumper
        fields = ('id', 'service_ip', 'normal_user','sshpasswd','sshport','info','status'
                )

class SystemTypeSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = System_Type
        fields = ('id','name')
