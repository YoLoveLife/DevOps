# -*- coding:utf-8 -*-
# !/usr/bin/env python
# Time 10 15:38
# Author Yo
# Email YoLoveLife@outlook.com
from django.conf.urls import url
from .. import views
from ..views import db as DBView
from ..views import redis as RedisView
urlpatterns = [
    #Resource db url
    url(r'^db/$',DBView.ApplicationDBListView.as_view(),name='db'),
    url(r'^db/create/$',DBView.ApplicationDBCreateView.as_view(),name='dbcreate'),
    url(r'^db/(?P<pk>[0-9]+)/update/',DBView.ApplicationDBUpdateView.as_view(),name='dbupdate'),
    url(r'^db/(?P<pk>[0-9]+)/detail/', DBView.ApplicationDBDetailView.as_view(), name='dbdetail'),
    url(r'^db/(?P<pk>[0-9]+)/auth/', DBView.ApplicationDBAuthView.as_view(), name='dbauth'),

    #Resource redis url
    url(r'^redis/$',RedisView.ApplicationRedisListView.as_view(),name='redis'),
    url(r'^redis/create/$',RedisView.ApplicationRedisCreateView.as_view(),name='rediscreate'),
    url(r'^redis/(?P<pk>[0-9]+)/update/',RedisView.ApplicationRedisUpdateView.as_view(),name='redisupdate'),
    url(r'^redis/(?P<pk>[0-9]+)/detail/', RedisView.ApplicationRedisDetailView.as_view(), name='redisdetail'),
]