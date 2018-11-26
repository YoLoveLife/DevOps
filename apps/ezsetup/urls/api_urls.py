# -*- coding:utf-8 -*-
# !/usr/bin/env python
# Time 18-7-3
# Author Yo
# Email YoLoveLife@outlook.com
from django.urls import path
from ezsetup.api import ezsetup as EZSetupAPI
urlpatterns = [
    # Resource EZSETUP Group Instance api
    path(r'v1/bypage/', EZSetupAPI.EZSetupListByPageAPI.as_view()),
    path(r'v1/redis/create/', EZSetupAPI.EZSetupCreateRedisAPI.as_view()),
]
