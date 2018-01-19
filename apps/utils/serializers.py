import models
from rest_framework import serializers

class JumperSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.Jumper
        fields = ('id', 'service_ip', 'normal_user','sshpasswd','sshport','info','status'
                )