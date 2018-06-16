# -*- coding: utf-8 -*-
from work import models
from rest_framework import serializers

__all__ = [
    'CodeWorkStatusSerializer', 'CodeWorkSerializer', 'CodeWorkCheckSerializer',
    'CodeWorkRunSerializer'
]


class CodeWorkStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Code_Work
        fields = (
            'id', 'status',
        )
        read_only_fields = (
            'id',
        )


class CodeWorkCheckSerializer(CodeWorkStatusSerializer):
    def update(self, instance, validated_data):
        instance.status = 2
        instance.save()
        return super(CodeWorkCheckSerializer,self).update(instance, {})


class CodeWorkRunSerializer(CodeWorkStatusSerializer):
    def update(self, instance, validated_data):
        instance.status = 4
        instance.save()
        return super(CodeWorkRunSerializer,self).update(instance,{})


class CodeWorkSerializer(serializers.HyperlinkedModelSerializer):
    mission = serializers.PrimaryKeyRelatedField(queryset=models.Mission.objects.all(), allow_null=True)
    push_mission = serializers.PrimaryKeyRelatedField(required=False,queryset=models.Push_Mission.objects.all(), allow_null=True)
    mission_info = serializers.CharField(source='mission.info', required=False, read_only=True)
    username = serializers.CharField(source='user.full_name', required=False, read_only=True)
    create_time = serializers.DateTimeField(source='push_mission.create_time', format="%Y-%m-%dT%H:%M:%S", read_only=True)
    finish_time = serializers.DateTimeField(source='push_mission.finish_time', format="%Y-%m-%dT%H:%M:%S", read_only=True)
    files = serializers.ListField(source='file_list', read_only=True)

    class Meta:
        model = models.Code_Work
        fields = (
            'id', 'uuid', 'info', 'mission', 'push_mission', 'mission_info', 'status', 'username', 'create_time', 'finish_time', 'files'
        )
        read_only_fields = (
            'id', 'uuid', 'push_mission', 'status', 'username', 'create_time', 'finish_time', 'files'
        )

    def create(self, validated_data):
        mission = validated_data.pop('mission')
        validated_data['user'] = self.context['request'].user
        # validated_data.pop('push_mission')
        push_obj = models.Push_Mission.objects.create(mission=mission)

        # 任务是否需要审核
        if mission.need_validate is True:
            push_obj.status = 0
        # 任务是否需要上传文件
        elif len(mission.file_list) != 0:
            push_obj.status = 1
        else:
            push_obj.status = 2
        push_obj.save()

        obj = models.Code_Work.objects.create(push_mission=push_obj, mission=mission, **validated_data)
        obj.save()
        return obj


class CodeWorkUploadFileSerializer(serializers.ModelSerializer):
    files = serializers.ListField(source="file_list")
    class Meta:
        model = models.Code_Work
        fields = (
            'id', 'files'
        )