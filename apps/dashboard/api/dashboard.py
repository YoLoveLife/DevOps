# -*- coding:utf-8 -*-
# !/usr/bin/env python
# Time 18-7-3
# Author Yo
# Email YoLoveLife@outlook.com
import redis
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.views import Response, status
from rest_framework.views import APIView
from deveops.api import WebTokenAuthentication
from django.conf import settings

__all__ = [
    "DashboardCountAPI", "DashboardGroupAPI", "DashboardWorkAPI",
]


class DashboardCountAPI(WebTokenAuthentication, APIView):
    permission_classes = [IsAuthenticated, ]

    def get(self, request, *args, **kwargs):
        connect = redis.StrictRedis(
            host=settings.REDIS_HOST,
            port=settings.REDIS_PORT,
            db=settings.REDIS_SPACE,
            password=settings.REDIS_PASSWD
        )
        TEMP = connect.hgetall('COUNT',)
        COUNT = {}
        for key in TEMP:
            COUNT[str(key, encoding='utf-8')] = TEMP[key]
        return Response(
            COUNT or {}, status.HTTP_200_OK
        )


class DashboardWorkAPI(WebTokenAuthentication, APIView):
    permission_classes = [IsAuthenticated,]

    def get(self, request, *args, **kwargs):
        connect = redis.StrictRedis(
            host=settings.REDIS_HOST,
            port=settings.REDIS_PORT,
            db=settings.REDIS_SPACE,
            password=settings.REDIS_PASSWD
        )
        week_list = ['Won', 'Tue', 'Wed', 'Thur', 'Fri', 'Sat', 'Sun']
        TEMP = connect.hgetall('WORK',)
        WORK = []
        for key in week_list:
            WORK.append({
                'time': str(key, encoding='utf-8'),
                '执行次数': TEMP[key]
            })
        return Response(
            {'title': '一周内工单执行','dataset': WORK} or {}, status.HTTP_200_OK
        )


class DashboardGroupAPI(WebTokenAuthentication, APIView):
    permission_classes = [IsAuthenticated, ]

    def get(self, request, *args, **kwargs):
        connect = redis.StrictRedis(
            host=settings.REDIS_HOST,
            port=settings.REDIS_PORT,
            db=settings.REDIS_SPACE,
            password=settings.REDIS_PASSWD
        )
        TEMP = connect.hgetall('GROUP',)
        GROUP = [
            ['主机数目','count'],
        ]
        for key in TEMP:
            GROUP.append([str(key, encoding='utf-8'), int(TEMP[key])])
        return Response(
            {'title': '主机统计', 'dataset': GROUP} or {}, status.HTTP_200_OK
        )
