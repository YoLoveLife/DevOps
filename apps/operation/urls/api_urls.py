from django.conf.urls import url, include
from rest_framework import routers
from .. import api
urlpatterns=[
    # Resource script api
    url(r'^v1/script/', api.ScriptListAPI.as_view()),

    # Resource script avrg api
    url(r'^v1/scriptargs/(?P<pk>[0-9]+)',api.ScriptArgsListAPI.as_view()),
]