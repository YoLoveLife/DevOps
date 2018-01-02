from django.conf.urls import url
from .. import api
urlpatterns=[
    # Resource softlib api
    url(r'^v1/softlib/$', api.SoftlibListAPI.as_view()),
]