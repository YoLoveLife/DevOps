from django.conf.urls import url, include
from rest_framework import routers
from .. import api
urlpatterns=[
    # Resource group api
    url(r'^v1/group/', api.GroupListAPI.as_view()),

    # Resource host api
    url(r'^v1/hostbygroup/(?P<pk>[0-9]+)',api.HostListByGroupAPI.as_view()),

    # Resource storage api
    url(r'^v1/storage/', api.StorageListAPI.as_view()),
    # url(r'^v1/storagebygroup/(?P<pk>[0-9]+)',api.StorageListByGroup.as_view()),

    # Resource systemtype api
    url(r'^v1/dashboard/systemtype',api.SystemTypeAPI.as_view()),

    # url(r'^v1/groupcreate/', api.GroupCreateAPI.as_view()),
    # url(r'^v1/hostcreate/',api.HostCreateAPI.as_view()),
    # url(r'^v1/storagecreate/',api.StorageCreateAPI.as_view()),
    # url(r'^v1/storagebygroup/(?P<pk>[0-9]+)',api.StorageListByGroup.as_view()),
    # url(r'^v1/hostupdate/(?P<pk>[0-9]+)/storages/',api.HostUpdateStorageApi.as_view()),
    # url(r'^v1/host-updategroup/(?P<pk>\d+)/',api.HostUpdateGroupApi.as_view()),
]