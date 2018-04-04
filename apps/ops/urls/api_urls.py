from django.conf.urls import url
from ..api import meta as MetaAPI
urlpatterns=[
    # Resource meta api
    url(r'^v1/meta/$', MetaAPI.OpsMetaListAPI.as_view()),
    url(r'^v1/meta/bypage/$', MetaAPI.OpsMetaListByPageAPI.as_view()),
    # url(r'^v1/meta/create/$', GroupAPI.ManagerGroupCreateAPI.as_view()),
    # url(r'^v1/meta/(?P<pk>[0-9]+)/detail/$', GroupAPI.ManagerGroupDetailAPI.as_view()),
    # url(r'^v1/meta/(?P<pk>[0-9]+)/update/$', GroupAPI.ManagerGroupUpdateAPI.as_view()),
    # url(r'^v1/meta/(?P<pk>[0-9]+)/delete/$', GroupAPI.ManagerGroupDeleteAPI.as_view()),
]