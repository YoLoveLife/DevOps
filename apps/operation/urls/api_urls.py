from django.conf.urls import url, include
from rest_framework import routers
from .. import api
urlpatterns=[
    # Resource script api
    url(r'^v1/script/$', api.ScriptListAPI.as_view()),

    url(r'^v1/script/(?P<pk>[0-9]+)/args/',api.ScriptArgsListAPI.as_view()),

    # Resource script  api
    url(r'^v1/script/(?P<pk>[0-9]+)/update/',api.ScriptUpdateArgsAPI.as_view()),

]