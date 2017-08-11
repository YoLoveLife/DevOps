from models import Script
from rest_framework import serializers
class ScriptSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Script
        fields = ('id', 'name', 'info','author'
                )