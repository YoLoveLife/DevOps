# -*- coding:utf-8 -*-
# !/usr/bin/env python
# Time 18-7-3
# Author Yo
# Email YoLoveLife@outlook.com
from rest_framework.permissions import IsAuthenticated,AllowAny
from deveops.api import WebTokenAuthentication
from rest_framework.views import Response, status
import redis, json
from rest_framework.views import APIView
from django.conf import settings

class DashboardSystypeAPI(WebTokenAuthentication, APIView):
    permission_classes = [AllowAny,]

    def get(self, request, *args, **kwargs):
        connect = redis.StrictRedis(host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=settings.REDIS_SPACE,
                                    password=settings.REDIS_PASSWD)
        SYSTEMTYPE_STATUS = str(connect.get('SYSTEMTYPE_STATUS'), encoding='utf-8').replace('\'', '"')
        try:
            SYSTEMTYPE_STATUS = json.loads(SYSTEMTYPE_STATUS)
        except TypeError as e:
            SYSTEMTYPE_STATUS = {"name":[],"value":[]}
        from pyecharts import Pie
        from pyecharts.base import TRANSLATOR
        p = Pie('操作系统类型', title_pos='center')
        p.add("操作系统", SYSTEMTYPE_STATUS.get('name'), SYSTEMTYPE_STATUS.get('value'), radius=[20, 65],
              legend_orient='vertical',)#is_legend_show=False,)
        snippet = TRANSLATOR.translate(p.options)
        return Response(json.loads((snippet.as_snippet())), status.HTTP_200_OK)


class DashboardGroupAPI(WebTokenAuthentication, APIView):
    permission_classes = [AllowAny,]

    def get(self, request, *args, **kwargs):
        connect = redis.StrictRedis(host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=settings.REDIS_SPACE,
                                    password=settings.REDIS_PASSWD)

        GROUP_STATUS = str(connect.get('GROUP_STATUS'), encoding='utf-8').replace('\'', '"')
        try:
            GROUP_STATUS = json.loads(GROUP_STATUS)
        except TypeError as e:
            GROUP_STATUS = {"name":[],"value":[]}
        from pyecharts import Pie
        from pyecharts.base import TRANSLATOR
        p = Pie('应用组类型', title_pos='center')
        p.add("应用组系统", GROUP_STATUS.get('name'), GROUP_STATUS.get('value'), radius=[20, 65],
              legend_orient='vertical', )
        snippet = TRANSLATOR.translate(p.options)
        return Response(json.loads((snippet.as_snippet())), status.HTTP_200_OK)