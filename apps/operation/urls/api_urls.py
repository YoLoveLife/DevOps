from django.conf.urls import url, include
from rest_framework import routers
from .. import api
urlpatterns=[
    # Resource script api
    url(r'^v1/script/', api.ScriptListAPI.as_view()),
]