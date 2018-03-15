# -*- coding:utf-8 -*-
# !/usr/bin/env python
# Time 10 15:38
# Author Yo
# Email YoLoveLife@outlook.com
from django.conf.urls import url
from .. import views
urlpatterns = [
    #Resource jumper url
    url(r'^jumper/$', views.UtilsJumperView.as_view(),name='jumper'),
    url(r'^jumper/create/$', views.UtilsJumperCreateView.as_view(),name='jumpercreate'),
    url(r'^jumper/(?P<pk>[0-9]+)/update/$',views.UtilsJumperUpdateView.as_view(),name='jumperupdate'),

    #Resource other url
    url(r'^other/$', views.UtilsView.as_view(),name='other'),
    url(r'^systype/(?P<pk>[0-9]+)/delete/$', views.UtilsSystemTypeDeleteView.as_view(),name='systypedelete'),
    url(r'^systype/create/$', views.UtilsSystemTypeCreateView.as_view(),name='systypecreate'),

    #Resource user url
    url(r'^user/$', views.UtilsUserView.as_view(),name='user'),
    # url(r'^user/create/$', views.UtilsUserCreateView.as_view(),name='usercreate'),
    # url(r'^user/(?P<pk>[0-9]+)/delete/$', views.UtilsUserDeleteView.as_view(),name='userdelete'),
]