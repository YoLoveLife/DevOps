from django.conf.urls import url
from ..api import work as WorkAPI
urlpatterns=[
    # Resource codework api
    url(r'^v1/codework/bypage/$', WorkAPI.CodeWorkListByPageAPI.as_view()),
    url(r'^v1/codework/create/$', WorkAPI.CodeWorkCreateAPI.as_view()),
    url(r'^v1/codework/(?P<pk>[0-9]+)/exam/', WorkAPI.CodeWorkExamAPI.as_view()),
    url(r'^v1/codework/(?P<pk>[0-9]+)/run/', WorkAPI.CodeWorkRunAPI.as_view()),
]