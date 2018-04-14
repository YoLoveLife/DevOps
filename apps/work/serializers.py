# -*- coding: utf-8 -*-
import models
from rest_framework import serializers

__all__ = [
    'CodeWorkSerializer',
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


class CodeStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Code_Work
        fields = (
            'id', 'status'
        )


class CodeWorkSerializer(serializers.HyperlinkedModelSerializer):
    mission = serializers.PrimaryKeyRelatedField(queryset=models.Mission.objects.all(), allow_null=True)
    push_mission = serializers.PrimaryKeyRelatedField(required=False,queryset=models.Push_Mission.objects.all(), allow_null=True)
    mission_info = serializers.CharField(source='mission.info', required=False, read_only=True)
    username = serializers.CharField(source='user.full_name', required=False, read_only=True)

    class Meta:
        model = models.Code_Work
        fields = (
            'id', 'uuid', 'info', 'mission', 'push_mission', 'mission_info', 'status', 'username'
        )
        read_only_fields = (
            'id', 'uuid', 'push_mission', 'status', 'username'
        )

    def create(self, validated_data):
        mission = validated_data.pop('mission')
        validated_data['user'] = self.context['request'].user
        # validated_data.pop('push_mission')
        push_obj = models.Push_Mission.objects.create(mission=mission)

        push_obj.validate = not mission.need_validate
        print(not mission.need_validate)
        push_obj.save()

        obj = models.Code_Work.objects.create(push_mission=push_obj, mission=mission, **validated_data)
        if mission.need_validate: # 需要验证
            obj.status = 0
        else:
            obj.status = 2
        obj.save()
        # 判断是否上传文件以及审核
        return obj