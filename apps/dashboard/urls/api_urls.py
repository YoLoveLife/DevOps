from django.urls import path
from ..api import manager as ManagerAPI
from ..api import expired as ExpiredAPI

urlpatterns=[
    # Resource dashboard api
    path(r'v1/manager/', ManagerAPI.DashboardManagerAPI.as_view()),
    #
    # Resource expire api
    path(r'v1/expired/ecs/bypage/', ExpiredAPI.DashboardExpiredECSAPI.as_view()),
    path(r'v1/expired/rds/bypage/', ExpiredAPI.DashboardExpiredRDSAPI.as_view()),
]