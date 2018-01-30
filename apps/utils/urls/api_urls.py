from django.conf.urls import url
from .. import api
urlpatterns=[
    # Resource utils api
    url(r'^v1/jumper/$', api.UtilsJumperListAPI.as_view()),
    url(r'^v1/jumper/(?P<pk>[0-9]+)/remove/', api.UtilsJumperRemoveAPI.as_view()),
]