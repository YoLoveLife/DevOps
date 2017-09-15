from django.conf.urls import url
from .. import api
urlpatterns=[
    # Resource group api
    url(r'^v1/music/', api.MusicListAPI.as_view()),
]