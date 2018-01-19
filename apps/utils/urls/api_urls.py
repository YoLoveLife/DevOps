from django.conf.urls import url
from .. import api
urlpatterns=[
    # Resource utils api
    url(r'^v1/jumper/$', api.UtilsJumperListAPI.as_view()),
    # url(r'^v1/group/(?P<pk>[0-9]+)/remove/',api.ManagerGroupRemoveAPI.as_view()),
]