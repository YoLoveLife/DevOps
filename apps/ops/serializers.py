import models
from rest_framework import serializers

__all__ = [
    "MetaSerializer"
]

class MetaSerializer(serializers.ModelSerializer):
    hosts = serializers.PrimaryKeyRelatedField(many=True, queryset=models.Host.objects.all())
    contents = serializers.PrimaryKeyRelatedField(many=True, queryset=models.META_CONTENT.objects.all())
    group = serializers.PrimaryKeyRelatedField(queryset=models.Group.objects.all())
    group_name = serializers.CharField(source="group.name")
    user_list = serializers.ListField(source="group.users_list_byhostname")
    class Meta:
        model = models.META
        fields = (
            'id', 'hosts', 'contents', 'group', 'group_name', 'user_list', 'uuid','info'
        )
        read_only_fields = (
            'id', 'uuid', 'user_list', 'group_name'
        )
