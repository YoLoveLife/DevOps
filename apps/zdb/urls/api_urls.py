from django.urls import path
from zdb.api import instance as InstanceAPI
from zdb.api import instance_group as InstanceGroupAPI
urlpatterns=[
    # Resource ZDB Group Instance api
    path(r'v1/instance/group/', InstanceGroupAPI.ZDBInstanceGroupListAPI.as_view()),
    path(r'v1/instance/group/bypage/', InstanceGroupAPI.ZDBInstanceGroupListByPageAPI.as_view()),
    path(r'v1/instance/group/create/', InstanceGroupAPI.ZDBInstanceGroupCreateAPI.as_view()),
    path(r'v1/instance/group/<uuid:pk>/update/', InstanceGroupAPI.ZDBInstanceGroupUpdateAPI.as_view()),
    path(r'v1/instance/group/<uuid:pk>/delete/', InstanceGroupAPI.ZDBInstanceGroupDeleteAPI.as_view()),

    # Resource ZDB Instance api
    path(r'v1/instance/', InstanceAPI.ZDBInstanceListAPI.as_view()),
    path(r'v1/instance/bypage/', InstanceAPI.ZDBInstanceListByPageAPI.as_view()),
    path(r'v1/instance/import/', InstanceAPI.ZDBInstanceImportAPI.as_view()),
    path(r'v1/instance/create/', InstanceAPI.ZDBInstanceCreateAPI.as_view()),
    path(r'v1/instance/<uuid:pk>/update/', InstanceAPI.ZDBInstanceUpdateAPI.as_view()),
    # path(r'v1/instance/detail/<uuid:pk>/update/', InstanceAPI.DBInstanceDetailUpdateAPI.as_view()),
    path(r'v1/instance/<uuid:pk>/delete/', InstanceAPI.ZDBInstanceDeleteAPI.as_view()),
]