import models
from rest_framework import serializers

class DBSerializer(serializers.HyperlinkedModelSerializer):
    host_name = serializers.CharField(source='host.hostname',read_only=True)
    service_ip = serializers.CharField(source='host.service_ip',read_only=True)
    class Meta:
        model = models.DB
        fields = ('id','host_name','port','datadir','service_ip',
                )
