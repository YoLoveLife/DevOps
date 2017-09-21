import models
from rest_framework import serializers
class ExecuteSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.Callback
        fields = ('id')