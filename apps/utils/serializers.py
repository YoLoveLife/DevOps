import models
from rest_framework import serializers

__all__ = [
    'FileSerializer',
]


class FileSerializer(serializers.ModelSerializer):
    user = serializers.CharField(source='user.name',read_only=True)

    class Meta:
        model = models.FILE
        fields = (
            'id', 'file', 'create_time', 'user', 'type','image'
        )
        read_only_fields = (
            'id', 'create_time'
        )

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super(FileSerializer,self).create(validated_data)