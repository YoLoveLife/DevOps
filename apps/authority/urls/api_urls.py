from django.conf.urls import url
from ..api import user
from ..api import group
from ..api import permission
from ..api import key
from ..api import jumper
urlpatterns=[
    #Resource login api
    url(r'^login/', user.UserLoginAPI.as_view()),
    url(r'^userinfo/', user.UserInfoAPI.as_view()),
    #
    # Resource user api
    url(r'^v1/user/$', user.UserListAPI.as_view()),
    url(r'^v1/user/bypage/$', user.UserListByPageAPI.as_view()),
    url(r'^v1/opsuser/$', user.UserOpsListAPI.as_view()),
    url(r'^v1/opsuser/bypage/$', user.UserOpsListByPageAPI.as_view()),
    url(r'^v1/user/(?P<pk>[0-9]+)/update/$', user.UserUpdateAPI.as_view()),
    url(r'^v1/user/(?P<pk>[0-9]+)/delete/$', user.UserDeleteAPI.as_view()),
    #
    # Resource group api
    url(r'^v1/group/$', group.GroupListAPI.as_view()),
    url(r'^v1/group/bypage/$', group.GroupListByPageAPI.as_view()),
    url(r'^v1/group/create/$', group.GroupCreateAPI.as_view()),
    url(r'^v1/group/(?P<pk>[0-9]+)/update/$', group.GroupUpdateAPI.as_view()),
    url(r'^v1/group/(?P<pk>[0-9]+)/delete/$', group.GroupDeleteAPI.as_view()),
    #
    # Resource key api
    url(r'^v1/key/$', key.KeyListAPI.as_view()),
    url(r'^v1/key/bypage/$', key.KeyListByPageAPI.as_view()),
    url(r'^v1/key/create/$', key.KeyCreateAPI.as_view()),
    url(r'^v1/key/(?P<pk>[0-9]+)/update/$', key.KeyUpdateAPI.as_view()),
    url(r'^v1/key/(?P<pk>[0-9]+)/delete/$', key.KeyDeleteAPI.as_view()),
    #
    # Resource jumper api
    url(r'^v1/jumper/$', jumper.JumperListAPI.as_view()),
    url(r'^v1/jumper/bypage/$', jumper.JumperListByPageAPI.as_view()),
    url(r'^v1/jumper/(?P<pk>[0-9]+)/status/$', jumper.JumperStatusAPI.as_view()),
    url(r'^v1/jumper/create/$', jumper.JumperCreateAPI.as_view()),
    url(r'^v1/jumper/(?P<pk>[0-9]+)/update/$', jumper.JumperUpdateAPI.as_view()),
    url(r'^v1/jumper/(?P<pk>[0-9]+)/delete/$', jumper.JumperDeleteAPI.as_view()),
    #
    # Resource permission api
    url(r'^v1/permission/$',permission.PermissionListAPI.as_view()),
    # url(r'^v1/permission/(?P<pk>[0-9]+)/add/(?P<pk>[0-9]+)/$', api.PermissionAddForGroup.as_view()),
]