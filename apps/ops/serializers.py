import models
from rest_framework import serializers


class MetaSerializer(serializers.ModelSerializer):
    hosts = serializers.PrimaryKeyRelatedField(many=True, queryset=models.Host.objects.all())
    contents = serializers.PrimaryKeyRelatedField(many=True, queryset=models.META_CONTENT.objects.all())
    group = serializers.PrimaryKeyRelatedField(queryset=models.Group.objects.all())

    class Meta:
        model = models.META
        fields = (
            'id', 'hosts', 'contents','group'
        )
        read_only_fields = (
            'id',
        )
