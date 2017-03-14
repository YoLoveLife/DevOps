# -*- coding:utf-8 -*-
# !/usr/bin/env python
# Time 10 15:38
# Author Yo
# Email YoLoveLife@outlook.com
from django.conf.urls import url,include
from django.conf.urls.static import static
from django.conf import settings
from django.contrib import admin
from . import views
urlpatterns = [
   url(r'^$',views.index,name='index'),
]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)