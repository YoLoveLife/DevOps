import models
from rest_framework import serializers

class SoftlibSerializer(serializers.HyperlinkedModelSerializer):
    softtype = serializers.CharField(source='get_soft_type_display')
    class Meta:
        model = models.Softlib
        fields = ('id', 'softtype', 'soft_version',
                )