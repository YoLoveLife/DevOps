# -*- coding:utf-8 -*-
# !/usr/bin/env python
# Time 09 13:50
# Author Yo
# Email YoLoveLife@outlook.com
from django.conf.urls import url
from ..views import user as UserView
urlpatterns = [
    #user
    url(r'^user/$', UserView.AuthorityUserView.as_view(), name='user'),
    url(r'^user/create/$',UserView.AuthorityUserCreateView.as_view(),name='usercreate'),
    url(r'^user/(?P<pk>[0-9]+)/update/',UserView.AuthorityUserUpdateView.as_view(),name='userupdate'),
]
