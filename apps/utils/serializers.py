from utils import models
from rest_framework import serializers

__all__ = [
    'FileSerializer', 'ImageSerializer',
]


class FileSerializer(serializers.ModelSerializer):
    user = serializers.CharField(source='user.full_name', read_only=True)
    mission_uuid = serializers.CharField(source='mission_used', read_only=True)

    class Meta:
        model = models.FILE
        fields = (
            'id', 'file', 'create_time', 'user', 'name', 'uuid', 'mission_uuid', 'var_name'
        )
        read_only_fields = (
            'id', 'create_time', 'uuid', 'mission_uuid',
        )

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super(FileSerializer,self).create(validated_data)


class ImageSerializer(serializers.ModelSerializer):
    user = serializers.CharField(source='user.name', read_only=True)

    class Meta:
        model = models.IMAGE
        fields = (
            'id', 'create_time', 'user', 'image', 'name', 'uuid'
        )
        read_only_fields = (
            'id', 'create_time', 'uuid'
        )

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super(ImageSerializer,self).create(validated_data)
