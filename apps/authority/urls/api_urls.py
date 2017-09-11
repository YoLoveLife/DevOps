from django.conf.urls import url
from .. import api
urlpatterns=[
    # Resource group api
    # url(r'^v1/group/', api.GroupListAPI.as_view()),

    # Resource user api
    url(r'^v1/user/',api.UserListAPI.as_view()),
]