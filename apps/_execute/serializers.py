from manager.models import Host
from application.models import DBDetail
from rest_framework import serializers

class UpdateHostSerializer(serializers.ModelSerializer):
    class Meta:
        model=Host
        fields = ('id','service_ip')

class CatchDBStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = DBDetail
        fields = ('id','com_insert','com_update','max_connections','thread_running')