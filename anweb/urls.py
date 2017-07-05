# -*- coding:utf-8 -*-
# !/usr/bin/env python
# Time 10 15:38
# Author Yo
# Email YoLoveLife@outlook.com
from django.conf.urls import url,include
from django.conf.urls.static import static
from django.conf import settings
from views import LoginView,IndexView
from . import views
urlpatterns = [
   url(r'^$',LoginView.as_view(),name='login'),
   url(r'^index/',IndexView.as_view(),name='index'),
]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)