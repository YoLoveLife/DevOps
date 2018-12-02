from django.urls import path
from timeline import api as TimeLineAPI
urlpatterns=[
    # Resource position api
    path(r'v1/bypage/', TimeLineAPI.TimeLineListByPageAPI.as_view()),
]