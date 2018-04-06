import models
from rest_framework import serializers

__all__ = [
    "MetaSerializer"
]


class MetaContentSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.META_CONTENT
        fields = (
            'id', 'name', 'module', 'args', 'sort'
        )
        read_only_fields = (
            'id',
        )


class MetaSerializer(serializers.ModelSerializer):
    hosts = serializers.PrimaryKeyRelatedField(many=True, queryset=models.Host.objects.all())
    contents = MetaContentSerializer(required=True, many=True, allow_null=True)
    group = serializers.PrimaryKeyRelatedField(queryset=models.Group.objects.all())
    group_name = serializers.CharField(source="group.name",read_only=True)

    class Meta:
        model = models.META
        fields = (
            'id', 'hosts', 'contents', 'group', 'group_name', 'uuid', 'info'
        )
        read_only_fields = (
            'id', 'uuid', 'group_name'
        )

    def create(self, validated_data):
        contents = validated_data.pop('contents')
        id_list = []
        for content in contents:
            content_instance = models.META_CONTENT.objects.create(**content)
            id_list.append(content_instance.id)

        hosts = validated_data.pop('hosts')

        contests_list = models.META_CONTENT.objects.filter(id__in=id_list)

        obj = models.META.objects.create(**validated_data)
        obj.contents.add(*contests_list)
        obj.hosts = hosts
        obj.save()

        return obj
        # detail_instance = models.HostDetail.objects.create(**detail)
        # validated_data.pop('groups')
        # return models.Host.objects.create(detail=detail_instance, **validated_data)

    def update(self, instance, validated_data):
        # print(validated_data)
        contents = validated_data.pop('contents')
        obj = super(MetaSerializer,self).update(instance,validated_data)
        return obj