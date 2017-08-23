from django.conf.urls import url
from apps.operation import api
urlpatterns=[
    # Resource script api
    url(r'^v1/script/$', api.ScriptListAPI.as_view()),

    url(r'^v1/script/(?P<pk>[0-9]+)/args/',api.ScriptArgsListAPI.as_view()),

    # Resource scriptargs api
    url(r'^v1/scriptargs/(?P<pk>[0-9]+)/create/',api.ScriptArgsCreateAPI.as_view()),
    url(r'^v1/scriptargs/(?P<pk>[0-9]+)/remove/',api.ScriptRemoveArgsAPI.as_view()),
]