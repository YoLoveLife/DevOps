from django.conf.urls import url
from ..api import file as FileAPI
urlpatterns=[
    # Resource file api
    url(r'^v1/file/$', FileAPI.UtilsFileListAPI.as_view()),
    url(r'^v1/file/bypage/$', FileAPI.UtilsFileListByPageAPI.as_view()),
    url(r'^v1/file/create/$', FileAPI.UtilsFileCreateAPI.as_view()),
    url(r'^v1/file/(?P<pk>[0-9]+)/delete/$', FileAPI.UtilsFileDeleteAPI.as_view())
]