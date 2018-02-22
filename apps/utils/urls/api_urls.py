from django.conf.urls import url
from .. import api
urlpatterns=[
    # Resource utils api
    url(r'^v1/jumper/$', api.UtilsJumperListAPI.as_view()),
    url(r'^v1/jumper/(?P<pk>[0-9]+)/remove/', api.UtilsJumperRemoveAPI.as_view()),

    # Resource systemtype api
    url(r'^v1/systype/$', api.UtilsSystemTypeListAPI.as_view()),
    url(r'^v1/systype/create/$', api.UtilsSystemTypeCreateAPI.as_view()),
    url(r'^v1/systype/(?P<pk>[0-9])/remove/$', api.UtilsSystemTypeRemoveAPI.as_view()),

    # Resource user api
    url(r'^v1/user/$', api.UtilsUserListAPI.as_view()),
]