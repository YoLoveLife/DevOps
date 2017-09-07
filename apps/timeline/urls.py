# -*- coding:utf-8 -*-
# !/usr/bin/env python
# Time 10 15:38
# Author Yo
# Email YoLoveLife@outlook.com
from django.conf.urls import url
import views
urlpatterns = [
    #Resource dashboard url
    url(r'^record/$',views.TimeLineRecordView.as_view(),name='timelinerecord'),
    url(r'^record/(?P<pk>[0-9]+)/list',views.TimeLineRecordListView.as_view(),name='timelinelist'),
    url(r'^record/(?P<pk>[0-9]+)/detail',views.TimeLineRecordDetailView.as_view(),name='timelinedetail'),
    url(r'^plan/$',views.TimeLinePlanView.as_view(),name='timelineplan'),
]