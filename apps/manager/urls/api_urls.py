from django.conf.urls import url, include
from rest_framework import routers
from .. import api
urlpatterns=[
    url(r'^v1/group/', api.GroupListAPI.as_view()),
    url(r'^v1/groupcreate/', api.GroupCreateAPI.as_view()),
    url(r'^v1/hostbygroup/(?P<pk>[0-9]+)',api.HostListByGroupAPI.as_view()),
    url(r'^v1/hostcreate/',api.HostCreateAPI.as_view()),
    url(r'^v1/storage/',api.StorageListAPI.as_view()),
    url(r'^v1/storagecreate/',api.StorageCreateAPI.as_view()),
    url(r'^v1/storagebygroup/(?P<pk>[0-9]+)',api.StorageListByGroup.as_view()),
]