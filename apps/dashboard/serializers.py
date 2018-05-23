# -*- coding:utf-8 -*-
from dashboard import models
from rest_framework import serializers

__all__ = [
    "DashboardExpiredAliyunECSSerializer", "DashboardExpiredAliyunRDSSerializer"
]


class DashboardExpiredAliyunECSSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ExpiredAliyunECS
        fields = (
            'id', 'status', 'connect_ip', 'tags', 'recognition_id', 'expired', 'instancename'
        )


class DashboardExpiredAliyunRDSSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ExpiredAliyunRDS
        fields = (
            'id', 'status', 'recognition_id', 'expired', 'instancename', 'version', 'readonly'
        )