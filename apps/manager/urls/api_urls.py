from django.conf.urls import url
from .. import api
urlpatterns=[
    # Resource group api
    url(r'^v1/group/', api.GroupListAPI.as_view()),

    # Resource host api
    url(r'^v1/hostbygroup/(?P<pk>[0-9]+)',api.HostListByGroupAPI.as_view()),

    # Resource storage api
    url(r'^v1/storage/', api.StorageListAPI.as_view()),

    # Resource systemtype api
    url(r'^v1/dashboard/systemtype',api.SystemTypeAPI.as_view()),

]