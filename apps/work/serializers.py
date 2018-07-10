# -*- coding: utf-8 -*-
from work import models
from django.conf import settings
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
        print(instance.file_list)
        if len(instance.file_list) != 0:
            print('OPS_PUSH_MISSION_WAIT_UPLOAD')
            instance.push_mission.status = settings.OPS_PUSH_MISSION_WAIT_UPLOAD
        else:
            print('OPS_PUSH_MISSION_WAIT_RUN')
            instance.push_mission.status = settings.OPS_PUSH_MISSION_WAIT_RUN
        instance.push_mission.save()
        return super(CodeWorkCheckSerializer,self).update(instance, {})


class CodeWorkRunSerializer(CodeWorkStatusSerializer):
    def update(self, instance, validated_data):
        instance.push_mission.status = settings.OPS_PUSH_MISSION_WAIT_RUN
        instance.save()
        return super(CodeWorkRunSerializer,self).update(instance, {})


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
        if mission.need_validate:
            push_obj.status = settings.OPS_PUSH_MISSION_WAIT_EXAM
        # 任务是否需要上传文件
        elif mission.file_list:
            push_obj.status = settings.OPS_PUSH_MISSION_WAIT_UPLOAD
        else:
            push_obj.status = settings.OPS_PUSH_MISSION_WAIT_RUN

        push_obj.save()

        obj = models.Code_Work.objects.create(push_mission=push_obj, mission=mission, **validated_data)

        return obj


class CodeWorkUploadFileSerializer(serializers.ModelSerializer):
    files = serializers.ListField(source="file_list")

    class Meta:
        model = models.Code_Work
        fields = (
            'id', 'files'
        )