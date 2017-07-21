from django.conf.urls import url, include
from rest_framework import routers
from .. import api

#router=routers.DefaultRouter()
#router.register(r'host',api.HostViewSet)
#router.register(r'group',api.GroupViewSet)
#urlpatterns=[
#    url(r'^host/(?P<pk>[0-9]+)', api.HostListAPI.as_view()),
#]
urlpatterns=[
    url(r'^v1/group/(?P<pk>[0-9]+)', api.GroupListAPI.as_view()),
    url(r'^v1/hostbygroup/(?P<pk>[0-9]+)',api.HostListByGroupAPI.as_view())
]
#urlpatterns+=router.urls