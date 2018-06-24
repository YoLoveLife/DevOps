from django.urls import path
from db import api as DBAPI
from db.api import instance as InstanceAPI
from db.api import role as RoleAPI
from db.api import user as UserAPI
urlpatterns=[
    # Resource DB Instance api
    path(r'v1/instance/', InstanceAPI.DBInstanceListAPI.as_view()),
    path(r'v1/instance/bypage/', InstanceAPI.DBInstanceListByPageAPI.as_view()),
    path(r'v1/instance/create/', InstanceAPI.DBInstanceCreateAPI.as_view()),
    path(r'v1/instance/<uuid:pk>/update/', InstanceAPI.DBInstanceUpdateAPI.as_view()),
    # path(r'v1/instance/detail/<uuid:pk>/update/', InstanceAPI.DBInstanceDetailUpdateAPI.as_view()),
    path(r'v1/instance/<uuid:pk>/delete/', InstanceAPI.DBInstanceDeleteAPI.as_view()),

    # Resource DB Role api
    path(r'v1/role/', RoleAPI.DBRoleListAPI.as_view()),
    path(r'v1/role/bypage/', RoleAPI.DBRoleListByPageAPI.as_view()),
    path(r'v1/role/create/', RoleAPI.DBRoleCreateAPI.as_view()),
    path(r'v1/role/<uuid:pk>/update/', RoleAPI.DBRoleUpdateAPI.as_view()),
    path(r'v1/role/<uuid:pk>/delete/', RoleAPI.DBRoleDeleteAPI.as_view()),
    #
    # Resource DB User api
    path(r'v1/user/', UserAPI.DBUserListAPI.as_view()),
    path(r'v1/user/bypage/', UserAPI.DBUserListByPageAPI.as_view()),
    path(r'v1/user/create/', UserAPI.DBUserCreateAPI.as_view()),
    path(r'v1/user/<uuid:pk>/update/', UserAPI.DBUserUpdateAPI.as_view()),
    path(r'v1/user/<uuid:pk>/delete/', UserAPI.DBUserDeleteAPI.as_view()),

]