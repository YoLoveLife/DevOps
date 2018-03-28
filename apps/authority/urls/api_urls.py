from django.conf.urls import url
from ..api import user
from ..api import group
from ..api import permission
from ..api import key
urlpatterns=[
    #Resource login api
    url(r'^login/', user.UserLoginAPI.as_view()),
    url(r'^userinfo/', user.UserInfoAPI.as_view()),
    #
    # Resource user api
    url(r'^v1/user/$', user.UserListAPI.as_view()),
    url(r'^v1/opsuser/$', user.UserOpsListAPI.as_view()),
    url(r'^v1/user/(?P<pk>[0-9]+)/update/$', user.UserUpdateAPI.as_view()),
    url(r'^v1/user/(?P<pk>[0-9]+)/delete/$', user.UserDeleteAPI.as_view()),
    #
    # Resource group api
    url(r'^v1/group/$', group.GroupListAPI.as_view()),
    url(r'^v1/group/create/$', group.GroupCreateAPI.as_view()),
    url(r'^v1/group/(?P<pk>[0-9]+)/update/$', group.GroupUpdateAPI.as_view()),
    url(r'^v1/group/(?P<pk>[0-9]+)/delete/$', group.GroupDeleteAPI.as_view()),
    #
    # Resource key api
    url(r'^v1/key/$', key.KeyListAPI.as_view()),
    url(r'^v1/key/create/$', key.KeyCreateAPI.as_view()),
    url(r'^v1/key/(?P<pk>[0-9]+)/update/$', key.KeyUpdateAPI.as_view()),
    url(r'^v1/key/(?P<pk>[0-9]+)/delete/$', key.KeyDeleteAPI.as_view()),
    #
    # Resource permission api
    url(r'^v1/permission/$',permission.PermissionListAPI.as_view()),
    # url(r'^v1/permission/(?P<pk>[0-9]+)/add/(?P<pk>[0-9]+)/$', api.PermissionAddForGroup.as_view()),
]