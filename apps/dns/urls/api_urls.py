from django.conf.urls import url
from .. import api
urlpatterns=[
    # Resource DNS api
    url(r'^v1/dns/$', GroupAPI.ManagerGroupListAPI.as_view()),
]