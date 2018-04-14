# -*- coding:utf-8 -*-
# !/usr/bin/env python
# Time 09 13:50
# Author Yo
# Email YoLoveLife@outlook.com
"""devEops URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url,include
from django.views.static import serve
from django.conf import settings
from rest_framework_jwt.views import obtain_jwt_token
import views
from . import api
urlpatterns = [
    # API
    url(r'^api-auth/', include('authority.urls.api_urls',namespace='api-auth')),
    url(r'^api-manager/', include('manager.urls.api_urls', namespace='api-manager')),
    url(r'^api-ops/', include('ops.urls.api_urls', namespace='api-ops')),
    url(r'^api-utils/', include('utils.urls.api_urls', namespace='api-utils')),
    url(r'^api-work/', include('work.urls.api_urls', namespace='api-work')),
    # url(r'^api-application/',include('application.urls.api_urls',namespace='api-application')),
    # url(r'^api-execute/',include('execute.urls.api_urls',namespace='api-execute')),
    # url(r'^api-softlib/',include('softlib.urls.api_urls',namespace='api-softlib')),
    # url(r'^api-utils/',include('utils.urls.api_urls',namespace='api-utils')),

    url(r'^media/(?P<path>.*)$', serve, {"document_root": settings.MEDIA_ROOT}),
]

'''
   
'''
