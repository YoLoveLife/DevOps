from django.conf.urls import url
from ..api import meta as MetaAPI
from ..api import mission as MissionAPI
from ..api import pushmission as Push_MissionAPI
urlpatterns=[
    # Resource meta api
    url(r'^v1/meta/$', MetaAPI.OpsMetaListAPI.as_view()),
    url(r'^v1/meta/bypage/$', MetaAPI.OpsMetaListByPageAPI.as_view()),
    url(r'^v1/meta/create/$', MetaAPI.OpsMetaCreateAPI.as_view()),
    url(r'^v1/meta/(?P<pk>[0-9]+)/update/$', MetaAPI.OpsMetaUpdateAPI.as_view()),
    url(r'^v1/meta/(?P<pk>[0-9]+)/delete/$', MetaAPI.OpsMetaDeleteAPI.as_view()),
    url(r'^v1/meta/(?P<pk>[0-9]+)/check/$', MetaAPI.OpsMetaNeedFileCheckAPI.as_view()),
    url(r'^v1/meta/(?P<pk>[0-9]+)/opsdir/$', MetaAPI.OpsMetaDirAPI.as_view()),
    # Resource mission api
    url(r'^v1/mission/$', MissionAPI.OpsMissionListAPI.as_view()),
    url(r'^v1/mission/byuser/$', MissionAPI.OpsMissionListByUserAPI.as_view()),
    url(r'^v1/mission/bypage/$', MissionAPI.OpsMissionListByPageAPI.as_view()),
    url(r'^v1/mission/create/$', MissionAPI.OpsMissionCreateAPI.as_view()),
    url(r'^v1/mission/(?P<pk>[0-9]+)/update/$', MissionAPI.OpsMissionUpdateAPI.as_view()),
    url(r'^v1/mission/(?P<pk>[0-9]+)/delete/$', MissionAPI.OpsMissionDeleteAPI.as_view()),
    # Resource push_mission api
    url(r'^v1/pushmission/$', Push_MissionAPI.OpsPushMissionCreateAPI.as_view()),
]