# -*- coding:utf-8 -*-
# !/usr/bin/env python
# Time 10 15:38
# Author Yo
# Email YoLoveLife@outlook.com
from django.conf.urls import url
from .. import views
urlpatterns = [
    #Resource dashboard url
    url(r'^jumper/$', views.UtilsJumperView.as_view(),name='jumper'),
    url(r'^jumper/create/$',views.UtilsJumperCreateModalView.as_view(),name='jumpercreate'),
    url(r'^jumper/(?P<pk>[0-9]+)/update/$',views.UtilsJumperUpdateModalView.as_view(),name='jumperupdate'),
]