import models
from rest_framework import serializers
__all__ = ['MusicSerializer']
class MusicSerializer(serializers.HyperlinkedModelSerializer):
    group_name = serializers.StringRelatedField(source="group.name",read_only=True)
    last_time = serializers.StringRelatedField(source="get_last_use_info",read_only=True)
    class Meta:
        model = models.Music
        fields = ('id', 'name', 'info','group_name','last_time'
                )