from django.urls import path
from ..api import group as GroupAPI
from ..api import systype as SystypeAPI
from ..api import position as PositionAPI
from ..api import host as HostAPI
urlpatterns=[
    # Resource group api
    path(r'v1/group/', GroupAPI.ManagerGroupListAPI.as_view()),
    path(r'v1/group/bypage/', GroupAPI.ManagerGroupListByPageAPI.as_view()),
    path(r'v1/group/create/', GroupAPI.ManagerGroupCreateAPI.as_view()),
    path(r'v1/group/<uuid:pk>/detail/', GroupAPI.ManagerGroupDetailAPI.as_view()),
    path(r'v1/group/<uuid:pk>/update/', GroupAPI.ManagerGroupUpdateAPI.as_view()),
    path(r'v1/group/<uuid:pk>/delete/', GroupAPI.ManagerGroupDeleteAPI.as_view()),
    path(r'v1/group/<int:pk>/selecthost/', GroupAPI.ManagerGroupSelectHostAPI.as_view()),
    #
    # Resource systype api
    path(r'v1/systype/', SystypeAPI.ManagerSysTypeListAPI.as_view()),
    path(r'v1/systype/create/', SystypeAPI.ManagerSysTypeCreateAPI.as_view()),
    path(r'v1/systype/<uuid:pk>/detail/', SystypeAPI.ManagerSysTypeDetailAPI.as_view()),
    path(r'v1/systype/<uuid:pk>/update/', SystypeAPI.ManagerSysTypeUpdateAPI.as_view()),
    path(r'v1/systype/<uuid:pk>/delete/', SystypeAPI.ManagerSysTypeDeleteAPI.as_view()),
    #
    # Resource position api
    path(r'v1/position/', PositionAPI.ManagerPositionListAPI.as_view()),
    path(r'v1/position/create/', PositionAPI.ManagerPositionCreateAPI.as_view()),
    path(r'v1/position/<uuid:pk>/detail/', PositionAPI.ManagerPositionDetailAPI.as_view()),
    path(r'v1/position/<uuid:pk>/update/', PositionAPI.ManagerPositionUpdateAPI.as_view()),
    path(r'v1/position/<uuid:pk>/delete/', PositionAPI.ManagerPositionDeleteAPI.as_view()),
    #
    # Resource host api
    path(r'v1/host/',HostAPI.ManagerHostListAPI.as_view()),
    path(r'v1/host/bypage/', HostAPI.ManagerHostListByPageAPI.as_view()),
    path(r'v1/host/create/', HostAPI.ManagerHostCreateAPI.as_view()),
    path(r'v1/host/<uuid:pk>/detail/byuuid/', HostAPI.ManagerHostDetailAPI.as_view()),
    path(r'v1/host/<str:pk>/detail/byalid/', HostAPI.ManagerAliyunIDDetailAPI.as_view()),
    path(r'v1/host/<uuid:pk>/update/', HostAPI.ManagerHostUpdateAPI.as_view()),
    path(r'v1/host/<uuid:pk>/delete/', HostAPI.ManagerHostDeleteAPI.as_view()),
    path(r'v1/host/<uuid:pk>/passwd/', HostAPI.ManagerHostPasswordAPI.as_view()),
    #
    # # Resource storage api
    # path(r'v1/storage/', api.ManagerStorageListAPI.as_view()),
    # path(r'v1/storage/(?P<pk>[0-9]+)/remove/', api.ManagerStorageRemoveAPI.as_view()),
]