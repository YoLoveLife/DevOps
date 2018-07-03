from django.urls import path
from ..api import monitor as MonitorAPI
urlpatterns=[
    # Resource host api
    path(r'v1/host/<uuid:pk>/cpu/aliyun/byuuid/', MonitorAPI.MonitorHostAliyunDetailCPUAPI.as_view()),
    path(r'v1/host/<uuid:pk>/memory/aliyun/byuuid/', MonitorAPI.MonitorHostAliyunDetailMemoryAPI.as_view()),
]