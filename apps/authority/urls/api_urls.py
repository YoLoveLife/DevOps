from django.conf.urls import url
from .. import api
urlpatterns=[
    #Resource login api
    url(r'^login/', api.LoginJSONWebToken.as_view()),
    url(r'^userinfo/', api.UserInfoJSONWebToken.as_view()),

    # Resource user api
    url(r'^v1/user/$',api.UserListAPI.as_view()),
    url(r'^v1/user/(?P<pk>[0-9]+)/update/$', api.UserUpdateAPI.as_view()),
    url(r'^v1/user/(?P<pk>[0-9]+)/delete/$', api.UserDeleteAPI.as_view()),

    # Resource group api
    url(r'^v1/group/$', api.GroupListAPI.as_view()),
    url(r'^v1/group/create/$', api.GroupCreateAPI.as_view()),
    url(r'^v1/group/(?P<pk>[0-9]+)/update/$', api.GroupUpdateAPI.as_view()),
    url(r'^v1/group/(?P<pk>[0-9]+)/delete/$', api.GroupDeleteAPI.as_view()),
    #

    url(r'^v1/permission/$',api.PermissionListAPI.as_view()),
    # url(r'^v1/permission/(?P<pk>[0-9]+)/add/(?P<pk>[0-9]+)/$', api.PermissionAddForGroup.as_view()),
]