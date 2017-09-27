from manager import models
from rest_framework import serializers

class UpdateHostSerializer(serializers.ModelSerializer):
    class Meta:
        model=models.Host
        fields = ('id','service_ip')