# -*- coding:utf-8 -*-
# !/usr/bin/env python
# Time 09 13:50
# Author Yo
# Email YoLoveLife@outlook.com
from django.conf.urls import url,include
from rest_framework import routers

from views import UserViewSet,GroupViewSet
router=routers.DefaultRouter()
router.register(r'users',UserViewSet)
router.register(r'groups',GroupViewSet)
urlpatterns = router.urls