from django.conf.urls import url
from .. import api
urlpatterns=[
    # Resource db api
    url(r'^v1/db/$', api.DBListAPI.as_view()),
    url(r'^v1/db/(?P<pk>[0-9]+)/remove/$',api.DBRemoveAPI.as_view()),
    url(r'^v1/db/(?P<pk>[0-9]+)/auth/$', api.DBAuthAPI.as_view()),
    url(r'^v1/db/(?P<pk>[0-9]+)/auth/create/$', api.DBAuthCreateAPI.as_view()),
    url(r'^v1/db/(?P<pk>[0-9]+)/auth/remove/$', api.DBAuthRemoveAPI.as_view()),

    # Resource redis api
    url(r'^v1/redis/$', api.RedisListAPI.as_view()),
]