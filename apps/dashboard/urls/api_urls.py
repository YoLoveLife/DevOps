from django.urls import path
from ..api import dashboard as DashboardAPI
from ..api import expired as ExpiredAPI

urlpatterns=[
    # Resource dashboard api
    path(r'v1/manager/', DashboardAPI.DashboardAPI.as_view()),
    #
    # Resource expire api
    path(r'v1/expired/ecs/bypage/', ExpiredAPI.DashboardExpiredECSAPI.as_view()),
    path(r'v1/expired/rds/bypage/', ExpiredAPI.DashboardExpiredRDSAPI.as_view()),
]