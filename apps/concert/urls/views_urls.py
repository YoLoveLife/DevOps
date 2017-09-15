# -*- coding:utf-8 -*-
# !/usr/bin/env python
# Time 10 15:38
# Author Yo
# Email YoLoveLife@outlook.com
from django.conf.urls import url
from .. import views
urlpatterns = [
    #Resource dashboard url
    # url(r'^dashboard/$', views.ManagerDashboardView.as_view(), name='dashboard'),

    #Resource music url
    url(r'^music/$', views.ConcertMusicListView.as_view(), name='music'),
    # url(r'^host/create/$',host.ManagerHostCreateView.as_view(),name='hostcreate'),
    # url(r'^host/(?P<pk>[0-9]+)/update/',host.ManagerHostUpdateView.as_view(),name='hostupdate'),
    # url(r'^host/(?P<pk>[0-9]+)/detail/',host.ManagerHostDetailView.as_view(),name='hostdetail'),
]