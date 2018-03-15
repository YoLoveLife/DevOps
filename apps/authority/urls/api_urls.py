from django.conf.urls import url
from .. import api
urlpatterns=[
    #Resource login api
    url(r'^login/', api.LoginJSONWebToken.as_view()),
    url(r'^userinfo/', api.UserInfoJSONWebToken.as_view()),

    # Resource user api
    url(r'^v1/user/$',api.UserListAPI.as_view()),
    url(r'^v1/user/(?P<pk>[0-9]+)/remove/$',api.UserRemoveAPI.as_view()),

    # Resource auth api
    url(r'^v1/auth/',api.AuthListAPI.as_view()),

    # Resource permission api
    url(r'^v1/permission/$',api.PermissionListAPI.as_view()),
    url(r'^v1/permission/(?P<pk>[0-9]+)/update/$',api.PermissionUpdateAPI.as_view()),
]