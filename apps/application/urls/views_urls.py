# -*- coding:utf-8 -*-
# !/usr/bin/env python
# Time 10 15:38
# Author Yo
# Email YoLoveLife@outlook.com
from django.conf.urls import url
from .. import views
from ..views import db as DBView
urlpatterns = [
    #Resource dashboard url
    url(r'^db/$',DBView.ApplicationDBListView.as_view(),name='appdb'),
]