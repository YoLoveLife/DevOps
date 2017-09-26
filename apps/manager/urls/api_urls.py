from django.conf.urls import url
from .. import api
urlpatterns=[
    # Resource group api
    url(r'^v1/group/', api.ManagerGroupListAPI.as_view()),

    # Resource host api
    url(r'^v1/hostbygroup/(?P<pk>[0-9]+)',api.ManagerHostListByGroupAPI.as_view()),

    # Resource storage api
    url(r'^v1/storage/', api.ManagerStorageListAPI.as_view()),

    # Resource search api
    url(r'^v1/search/',api.ManagerSearchAPI.as_view()),
]