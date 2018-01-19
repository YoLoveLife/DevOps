# -*- coding:utf-8 -*-
# !/usr/bin/env python
# Time 10 15:38
# Author Yo
# Email YoLoveLife@outlook.com
from django.conf.urls import url
from xmt import views
urlpatterns = [
    #Resource dashboard url
    url(r'^create/$', views.XMTCreateView.as_view(), name='create'),
    url(r'^result/(?P<pk>[0-9]+)/', views.XMTResultView.as_view(), name='result')
]