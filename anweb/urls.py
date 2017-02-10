# -*- coding:utf-8 -*-
# !/usr/bin/env python
# Time 10 15:38
# Author Yo
# Email YoLoveLife@outlook.com
from django.conf.urls import url,include

from django.contrib import admin
from . import views
urlpatterns = [
   url(r'^test/',views.test,name='test'),
]