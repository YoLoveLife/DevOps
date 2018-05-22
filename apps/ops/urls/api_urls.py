from django.urls import path
from ..api import meta as MetaAPI
from ..api import mission as MissionAPI
from ..api import pushmission as Push_MissionAPI
urlpatterns=[
    # Resource meta api
    path(r'v1/meta/', MetaAPI.OpsMetaListAPI.as_view()),
    path(r'v1/meta/bypage/', MetaAPI.OpsMetaListByPageAPI.as_view()),
    path(r'v1/meta/create/', MetaAPI.OpsMetaCreateAPI.as_view()),
    path(r'v1/meta/<uuid:pk>/update/', MetaAPI.OpsMetaUpdateAPI.as_view()),
    path(r'v1/meta/<uuid:pk>/delete/', MetaAPI.OpsMetaDeleteAPI.as_view()),
    # Resource mission api
    path(r'v1/mission/', MissionAPI.OpsMissionListAPI.as_view()),
    path(r'v1/mission/byuser/', MissionAPI.OpsMissionListByUserAPI.as_view()),
    path(r'v1/mission/bypage/', MissionAPI.OpsMissionListByPageAPI.as_view()),
    path(r'v1/mission/<uuid:pk>/playbook/', MissionAPI.OpsMissionPlaybookAPI.as_view()),
    path(r'v1/mission/<uuid:pk>/checkfile/', MissionAPI.OpsMissionNeedFileCheckAPI.as_view()),
    path(r'v1/mission/create/', MissionAPI.OpsMissionCreateAPI.as_view()),
    path(r'v1/mission/<uuid:pk>/update/', MissionAPI.OpsMissionUpdateAPI.as_view()),
    path(r'v1/mission/<uuid:pk>/delete/', MissionAPI.OpsMissionDeleteAPI.as_view()),
    # Resource push_mission api
    # path(r'v1/pushmission/', Push_MissionAPI.OpsPushMissionCreateAPI.as_view()),
]