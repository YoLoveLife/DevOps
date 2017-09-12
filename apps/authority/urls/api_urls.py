from django.conf.urls import url
from .. import api
urlpatterns=[
    # Resource user api
    url(r'^v1/user/',api.UserListAPI.as_view()),
]