# -*- coding:utf-8 -*-
# !/usr/bin/env python
# Time 10 15:38
# Author Yo
# Email YoLoveLife@outlook.com
from django.conf.urls import url
from rest_framework import viewsets
from .. import views

urlpatterns = [
    #Resource host url
    url(r'^host/$', views.ManagerHostListView.as_view(), name='host'),
    url(r'^host/create/$',views.ManagerHostCreateView.as_view(),name='hostcreate'),
    url(r'^host/(?P<pk>[0-9]+)/update/',views.ManagerHostUpdateView.as_view(),name='hostupdate'),

    #Resource group url
    url(r'^group/$', views.ManagerGroupListView.as_view(), name='group'),
    url(r'^group/create/$', views.ManagerGroupCreateView.as_view(), name='groupcreate'),
    url(r'^group/(?P<pk>[0-9]+)/update/', views.ManagerGroupUpdateView.as_view(), name='groupupdate'),

    url(r'^search$',views.ManagerSearchListView.as_view(),name='search'),
    url(r'^storage$',views.ManagerStorageListView.as_view(),name='storage'),
]