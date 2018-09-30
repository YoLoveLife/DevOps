from django.urls import path
from ..api import expired as ExpiredAPI
from ..api import dashboard as DashboardAPI
urlpatterns=[
    # Resource dashboard api
    path(r'v1/count/', DashboardAPI.DashboardCountAPI.as_view()),
    path(r'v1/work/', DashboardAPI.DashboardWorkAPI.as_view()),
    path(r'v1/group/', DashboardAPI.DashboardGroupAPI.as_view()),
    #
    # Resource expire api
    path(r'v1/expired/ecs/bypage/', ExpiredAPI.DashboardExpiredECSAPI.as_view()),
    path(r'v1/expired/rds/bypage/', ExpiredAPI.DashboardExpiredRDSAPI.as_view()),
    path(r'v1/expired/kvstore/bypage/', ExpiredAPI.DashboardExpiredKVStoreAPI.as_view()),
    path(r'v1/expired/mongodb/bypage/', ExpiredAPI.DashboardExpiredMongoDBAPI.as_view()),
]