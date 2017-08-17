# -*- coding:utf-8 -*-
# !/usr/bin/env python
# Time 10 15:38
# Author Yo
# Email YoLoveLife@outlook.com
from django.conf.urls import url
from ..views import script
urlpatterns = [
    #Resource script url
    url(r'^script/$', script.OperationScriptListView.as_view(), name='script'),
    url(r'^script/create/$',script.OperationScriptCreateView.as_view(),name='scriptcreate'),
    url(r'^script/(?P<pk>[0-9]+)/script/',script.OperationScriptUpdateView.as_view(),name='scriptupdate'),
]